---
title: "Elasticsearch 常见概念汇总"
subtitle: ""

init_date: "2023-09-12T21:19:02+08:00"

date: 2023-09-12

lastmod: 2023-09-12

draft: true

author: "xiaobinqt"
description: "xiaobinqt,"

featuredImage: ""

featuredImagePreview: ""

reproduce: false

translate: false

tags: [ "elasticsearch" ]
categories: [ "开发者手册" ]
lightgallery: true

series: [ ]

series_weight:

toc: true

math: true
---

<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 基本概念

**index 索引**：索引类似于 mysql 中的数据库，Elasticsearch 中的索引是存在数据的地方，包含了一堆有相似结构的文档数据。

**type 类型**：类型是用来定义数据结构，可以认为是 mysql 中的一张表，type 是 index 中的一个逻辑数据分类

**document 文档**：类似于 MySQL 中的一行，不同之处在于 ES 中的每个文档可以有不同的字段，但是对于通用字段应该具有相同的数据类型，文档是 es 中的最小数据单元，可以认为一个文档就是一条记录。

**field 字段**：field 是 Elasticsearch 的最小单位，一个 document 里面有多个 field

**shard 分片**：单台机器无法存储大量数据，es 可以将一个索引中的数据切分为多个 shard，分布在多台服务器上存储。有了 shard 就可以横向扩展，存储更多数据，让搜索和分析等操作分布到多台服务器上去执行，提升吞吐量和性能。

**replica 副本**：任何一个服务器随时可能故障或宕机，此时 shard 可能会丢失，因此可以**为每个 shard 创建多个 replica 副本**。replica 可以在 shard 故障时提供备用服务，保证数据不丢失，多个 replica 还可以提升搜索操作的吞吐量和性能。

## 应用场景

目前在互联网和电商方向，有很多都是用 ES 为 MySQL 去补齐短板的。最最典型的是两个应用场景：**全文检索** 和 **复杂查询**。尤其是复杂查询，因为 MySQL 的底层是通过 B+ Tree 实现的索引，如果把每个搜索项都建上索引，会非常影响 MySQL 的写入操作的性能。

如果业务主表的数据量过于庞大，MySQL 不得已做了分库分表方案的话，那会对 MySQL 的查询产生进一步的影响。因为查询条件里面如果不将分库分表键带入的话，就只能将 MySQL 已分的全部库表全部查询一遍，才会获取全部数据结果。基本上在互联网或电商领域引入ES，80% 都是为了解决这种场景的问题。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230913/c93ae9c025a34ff184b72a1d4fb42408.png '应用场景')

## 倒排索引

索引的初衷，是为了从一个海量数据集中快速找出某个字段等于确定值所对应的记录，索引分为正排索引和倒排索引两种。

正排索引，也叫正向索引（Forward Index），是通过文档 ID 去查找关键词（文档内容）。

倒排索引，也叫反向索引（Inverted Index），是通过关键词查找文档 ID。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230913/db4afacd2bce4417bddcc53f03f57d12.png '索引分类')

如果通过正排索引查找关键词 “elasticsearch” 时，需要遍历所有文档，查找出这个关键词所在的文档。如果文档数量非常庞大的话，正排索引的弊端就是查询效率太低。

而倒排索引的玩法就完全不一样了，通过倒排索引获得 “elasticsearch” 对应的文档 id 列表 1，再通过正排索引查询1所对应的文档，这样就可以了。

倒排索引包括两部分：词典（Term Dictionary） + 倒排列表（Posting List）。

单词词典（Term Dictionary）：记录了所有文档的单词与倒排列表的关联关系，单词词典会比较大，一般通过 B+ 树来实现，以满足高性能的插入与查询。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230913/2eb9f449c02344cbbf462c3aa3b19252.png '单词词典')

倒排列表（Posting List）：记录了单词对应的文档结合，由倒排索引项组成，包括：

- 文档 ID，等同于数据库主键；
- 词频（Term Frequency），该单词在文档中出现的次数，主要是用于打分；
- 位置（Position），单词在文档中分词的位置，用于语句搜索；
- 偏移（Offset），记录单词的的位置；

默认情况下，ES 的 JSON 文档中的每个字段，都有自己的倒排索引，这也其在复杂查询上优于 MySQL 的原因。

### DocValues

倒排索引也是有缺陷的，假如我们需要对数据做一些聚合操作，比如排序/分组时，lucene 内部会遍历提取所有出现在文档集合的排序字段，然后再构建一个最终的排好序的文档集合 list，这个步骤的过程全部维持在内存中操作，而且如果排序数据量巨大的话，非常容易就造成内存溢出和性能缓慢。

DocValues 就是 es 在构建倒排索引的同时，构建了正排索引，保存了 docId 到各个字段值的映射，可以看作是以文档为维度，从而实现根据指定字段进行排序和聚合的功能。

另外 docValues 保存在操作系统的磁盘中，当 docValues 大于节点的可用内存，ES 可以从操作系统页缓存中加载或弹出，从而避免发生内存溢出的异常，docValues 远小于节点的可用内存，操作系统自然将所有 docValues 存于内存中（堆外内存），有助于快速访问。

### text 和 keyword 类型的区别

keyword 类型是不会分词的，直接根据字符串内容建立倒排索引，keyword 类型的字段只能通过精确值搜索到；Text 类型在存入 Elasticsearch 的时候，会先分词，然后根据分词后的内容建立倒排索引

### 停顿词过滤

停顿词可以看成是没有意义的词，比如 “的”、“而”，这类词没有必要建立索引

## 分词器

说到倒排索引，就不得不提分词器，没有分词器的话，就没有词典，也就构建不了倒排索引了。分词器的主要工作是，把用户输入的一段文本，按照一定的逻辑，转换成一系列单词。

当然，仅仅这些还不够，因为单词中肯定是有重复的，接下来要做事情就是去重，以及去重之后的排序，这样便于搜索。

整体步骤如下：

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230913/43817a5b1775450cbdb44dc8fa0bd7cc.png '分词步骤')

分词器一般由三个部分组成：

- 字符过滤器（Character Filters），对原始文本进行处理，最常见的就是第一种 ；

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230913/cb2c14eedf8142d1baa3bbacc973db1a.png '字符过滤')

- 分词器（Tokenizer），顾名思义，将原始文本按照特定的规则切分为单词，默认的是 Standard Tokenizer；

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230913/56e2b7ab96a3444eab741756aedca81c.png '分词器')

- Token过滤器（Token Filter），将切分的单词进行加工，如：大小写转换，去掉停用词，加入同义词，等等。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230913/ecff9d7295804222bb311d52d12ad3bd.png '过滤器')

三者顺序为：

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230913/33b04bfa2e4c421a95a8743f7813dd51.png '顺序')

## 准实时搜索

随着按段（per-segment）搜索的发展，一个新的文档从索引到可被搜索的延迟显著降低了。新文档可做到在几分钟之内即可被检索，但这样依然不够快，不能满足于所有场景需求。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230913/4eaafe70bf7f486493732fd65159e632.png 'search')

磁盘在这里成为了瓶颈。因为，提交（Committing）一个新的段（Segment）到磁盘，需要一个 fsync 来确保段被物理性地写入磁盘，这样在断电的时候就不会丢失数据。但是，如果每次索引一个文档都去执行一次 fsync 的话，会造成很大的性能问题。

这里需要的是一个更轻量的方式来使一个文档可被搜索，在 ES 和磁盘之间是文件系统缓存。在内存索引缓冲区中的文档会被写入到一个新的段中，这里新段会被先写入到文件系统缓存（这一步代价会比较低），稍后再被刷新到磁盘（这一步代价比较高）。不过只要文件已经在缓存中， 就可以像其它文件一样被打开和读取了。

ES 的底层实现是 Lucene。而 Lucene 允许新段被写入和打开，使其包含的文档在未进行一次完整提交时便对搜索可见。这种方式比进行一次提交代价要小得多，并且在不影响性能的前提下可以被频繁地执行。

通过如上实现方式，可将 ES 可被检索的时长从分钟级别，优化到了秒级别。默认情况下，每个分片会每秒自动刷新（refresh）一次。这就是为什么说 ES 是近实时搜索。文档的变化并不是立即对搜索可见，但会在一秒之内变为可见。

refresh 的相关 API 如下：

（1）刷新（Refresh）所有的索引

```
POST /_refresh
```

（2）只刷新（Refresh）blogs 索引

```
POST /blogs/_refresh
```

（3）每30秒刷新 my_index 索引

```
PUT my_index/_settings
{
"index" : {
"refresh_interval" : "30s"
}
}
```

`refresh_interval` 可以在既存索引上进行动态更新。在生产环境中，当正在建立一个大的新索引时，可以先关闭自动刷新，待开始使用该索引时，再把它们调回来。

（4）关闭自动刷新 my\_index 索引，当内存缓冲区满了才进行 refresh 操作

```
PUT my_index/_settings
{
"index" : {
"refresh_interval" : "-1"
}
}
```

## 搜索类型（SearchType）

```
GET /_search?search_type=query_then_fetch
```

共有四种搜索类型，包括：query and fetch、query then fetch（默认）、DFS query and fetch 和 DFS query then fetch。

**query and fetch（本地）**

向索引的所有分片（shard）都发出查询请求，各分片返回的时候把元素文档（document）和计算后的排名分值一起返回。

优点：快。

缺点：排名不准确（每个分片计算后的分值进行排序），同时各个 shard 返回的结果的数量之和可能是用户要求的 size 的 n 倍。（数据量不准确）

**query then fetch（默认）（本地）**

先向所有的 shard 发出请求，各分片只返回文档 id（不包括文档 document）和排名分值（基于自己分片），然后按照各分片返回的文档的分数进行重新排名，取前 size 个文档。

根据文档 id 去相关的 shard 取 document，这种方式返回的 document 数量与用户要求的大小是相等的。

优点：返回的数据量是准确的。

缺点：性能一般，并且数据排名不准确。

**DFS query and fetch（全局）**

这种方式比第一种方式多了一个 DFS 步骤，有这一步，可以更精确控制搜索打分和排名。也就是在进行查询之前，先对所有分片发送请求，把所有分片中的词频率和文档频率等打分依据全部汇总到一块，再执行后面的操作。

优点：数据排名准确。

缺点：性能一般，返回的数据量不准确， 可能返回 (N\*分片数量) 的数据。

**DFS query then fetch（全局）**

比第 2 种方式多了一个 DFS 步骤。也就是在进行查询之前，先对所有分片发送请求，把所有分片中的词频率和文档频率等打分依据全部汇总到一块，再执行后面的操作。

优点：返回的数据量是准确的，数据排名准确。

缺点：性能最差

**DFS是一个什么样的过程?**

多了一个初始化散发（initial scatter）步骤，在进行真正的查询之前，先把各个分片的词频率和文档频率（排名信息）收集一下，然后进行词搜索的时候，各分片依据全局的词频率和文档频率进行搜索和排名。

**检索词的频率**

检索词 honeymoon 在这个文档的 tweet 字段中出现的次数。

**反向文档频率**

检索词 honeymoon 在索引上所有文档的 tweet 字段中出现的次数。

在每一个分片上查询符合要求的数据，并根据全局的 Term 和 Document 的频率信息计算相关性得分构建一个优先级队列存储查询结果（包含分页、排序，等等），把查询结果的metadata返回给查询节点。

注意，真正的文档此时还并没有返回，返回的只是得分数据。

## query 和 filter

ElasticSearch 中的 search 操作包括两种，查询（query）和过滤（filter）。

从使用场景的角度来看，**全文检索以及任何使用相关性评分的场景使用 query 查询，除此之外的使用 filter 过滤器进行过滤**。

示例如下：

```
GET /_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "title":   "Search" }},
        { "match": { "content": "Elasticsearch" }}
      ],
      "filter": [
        { "term":  { "status": "published" }},
        { "range": { "publish_date": { "gte": "2015-01-01" }}}
      ]
    }
  }
}
```

**query**：

此文档与此查询子句的匹配程度如何 ？以及 query 上下文的条件是用来给文档打分的，匹配越好 \_score 越高。

即：全文搜索，评分排序，无法缓存，性能低。

**filter**：

此文档和查询子句匹配吗？以及 filter 的条件只产生两种结果：符合与不符合，后者被过滤掉。

即：精确查询，是非过滤，可缓存，性能高。

**Query 检索细化关注点**

**是否包含**，确定文档是否应该成为结果的一部分。

**相关度得分**，除了确定文档是否匹配外，查询子句还计算了表示文档与其他文档相比匹配程度的\_score。得分越高，相关度越高。更相关的文件，在搜索排名更高。

**典型应用场景：**

（1）全文检索——这种相关性的概念非常适合全文搜索，因为很少有完全正确的答案。

如：文档中存在字段 hotel\_name：“上海浦东香格里拉酒店”，实际分词结果为：上海浦，上海，浦东，香格里拉，格里，里拉，酒店。也就是说，搜索以上关键词都能搜到：hotel\_name：“上海浦东香格里拉酒店” 的酒店。这些都是 “相关” 的。

（2）包含单词 “run”， 但也匹配 "runs", "running", "jog" 或者 "sprint"。（都是奔跑的意思）

**filter过滤细化关注点**

**是否包含**，确定是否包含在检索结果中，回答只有 “是” 或 “否”。

**不涉及评分**，在搜索中没有额外的相关度排名。

**针对结构化数据**，适用于完全精确匹配，范围检索。

**典型应用场景：**

（1）时间戳 timestamp 是否在2015至2016年范围内？

（2）状态字段 status 是否设置为 “published”？

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230913/7804eece4a594562b2dac4944c44c745.png ' ')

**为什么 filter 比 query 更快？**

因为，经常使用的过滤器将被 ES 自动缓存，以提高性能。只确定是否包括结果中，不需要考虑得分。

## ES的写入流程

### es 写数据的过程

![](https://pic3.zhimg.com/v2-a468ed9b2f391a583d5ae108751d15de_b.jpg)

（1）客户端选择一个 node 发送请求过去，这个 node 就是 coordinating node （协调节点）

（2）coordinating node 对 document 进行路由，将请求转发给对应的 node（有 primary shard）

（3）实际的 node 上的 primary shard 处理请求，然后将数据同步到 replica node

（4）coordinating node 等到 primary node 和所有 replica node 都执行成功之后，就返回响应结果给客户端。

### 写数据的底层原理

![](https://pic1.zhimg.com/v2-e3bf24593561b2794715a33e103e5e2c_b.jpg)

（1）数据先写入 memory buffer，然后定时（默认每隔1s）将 memory buffer 中的数据写入一个新的 segment 文件中，并进入 Filesystem cache（同时清空 memory buffer），这个过程就叫做 refresh；

ES 的近实时性：数据存在 memory buffer 时是搜索不到的，只有数据被 refresh 到 Filesystem cache 之后才能被搜索到，而 refresh 是每秒一次， 所以称 es 是近实时的，可以通过手动调用 es 的 api 触发一次 refresh 操作，让数据马上可以被搜索到；

（2）由于 memory Buffer 和 Filesystem Cache 都是基于内存，假设服务器宕机，那么数据就会丢失，所以 ES 通过 translog 日志文件来保证数据的可靠性，在数据写入 memory buffer 的同时，将数据写入 translog 日志文件中，在机器宕机重启时，es 会自动读取 translog 日志文件中的数据，恢复到 memory buffer 和 Filesystem cache 中去。

ES 数据丢失的问题：translog 也是先写入 Filesystem cache，然后默认每隔 5 秒刷一次到磁盘中，所以默认情况下，可能有 5 秒的数据会仅仅停留在 memory buffer 或者 translog 文件的 Filesystem cache中，而不在磁盘上，如果此时机器宕机，会丢失 5 秒钟的数据。也可以将 translog 设置成每次写操作必须是直接 fsync 到磁盘，但是性能会差很多。

（3）flush 操作：不断重复上面的步骤，translog 会变得越来越大，当 translog 文件默认每30分钟或者 阈值超过 512M 时，就会触发 commit 操作，即 flush操作。

- 将 buffer 中的数据 refresh 到 Filesystem Cache 中去，清空 buffer；
- 创建一个新的 commit point（提交点），同时强行将 Filesystem Cache 中目前所有的数据都 fsync 到磁盘文件中；
- 删除旧的 translog 日志文件并创建一个新的 translog 日志文件，此时 commit 操作完成

## ES的更新和删除流程

删除和更新都是写操作，但是由于 Elasticsearch 中的文档是不可变的，因此不能被删除或者改动以展示其变更；所以 ES 利用 .del 文件 标记文档是否被删除，磁盘上的每个段都有一个相应的.del 文件

（1）如果是删除操作，文档其实并没有真的被删除，而是在 .del 文件中被标记为 deleted 状态。该文档依然能匹配查询，但是会在结果中被过滤掉。

（2）如果是更新操作，就是将旧的 doc 标识为 deleted 状态，然后创建一个新的 doc。

memory buffer 每 refresh 一次，就会产生一个 segment 文件 ，所以默认情况下是 1s 生成一个 segment 文件，这样下来 segment 文件会越来越多，此时会定期执行 merge。

每次 merge 的时候，会将多个 segment 文件合并成一个，同时这里会将标识为 deleted 的 doc 给物理删除掉，不写入到新的 segment 中，然后将新的 segment 文件写入磁盘，这里会写一个 commit point ，标识所有新的 segment 文件，然后打开 segment 文件供搜索使用，同时删除旧的 segment 文件

## ES的搜索流程

搜索被执行成一个两阶段过程，即 Query Then Fetch：

### Query阶段

客户端发送请求到 coordinate node，协调节点将搜索请求广播到所有的 primary shard 或 replica shard。每个分片在本地执行搜索并构建一个匹配文档的大小为 from + size 的优先队列。每个分片返回各自优先队列中 所有文档的 ID 和排序值 给协调节点，由协调节点及逆行数据的合并、排序、分页等操作，产出最终结果。

### Fetch阶段

协调节点根据 doc id 去各个节点上查询实际的 document 数据，由协调节点返回结果给客户端。

- coordinate node 对 doc id 进行哈希路由，将请求转发到对应的 node，此时会使用 round-robin 随机轮询算法，在 primary shard 以及其所有 replica 中随机选择一个，让读请求负载均衡。
- 接收请求的 node 返回 document 给 coordinate node 。
- coordinate node 返回 document 给客户端。

Query Then Fetch 的搜索类型在文档相关性打分的时候参考的是本分片的数据，这样在文档数量较少的时候可能不够准确，DFS Query Then Fetch 增加了一个预查询的处理，询问 Term 和 Document frequency，这个评分更准确，但是性能会变差。

## 高并发下如何保证读写一致性

（1）对于更新操作：可以通过版本号使用乐观并发控制，以确保新版本不会被旧版本覆盖

每个文档都有一个`_version` 版本号，这个版本号在文档被改变时加一。Elasticsearch使用这个 `_version` 保证所有修改都被正确排序。当一个旧版本出现在新版本之后，它会被简单的忽略。

利用 `_version` 的这一优点确保数据不会因为修改冲突而丢失。比如指定文档的version来做更改。如果那个版本号不是现在的，我们的请求就失败了。

（2）对于写操作，一致性级别支持 quorum/one/all，默认为 quorum，即只有当大多数分片可用时才允许写操作。但即使大多数可用，也可能存在因为网络等原因导致写入副本失败，这样该副本被认为故障，分片将会在一个不同的节点上重建。

- **one**：要求我们这个写操作，只要有一个primary shard是active活跃可用的，就可以执行
- **all**：要求我们这个写操作，必须所有的primary shard和replica shard都是活跃的，才可以执行这个写操作
- **quorum**：默认的值，要求所有的shard中，必须是大部分的shard都是活跃的，可用的，才可以执行这个写操作

（3）对于读操作，可以设置 replication 为 sync(默认)，这使得操作在主分片和副本分片都完成后才会返回；如果设置replication 为 async 时，也可以通过设置搜索请求参数`_preference` 为 primary 来查询主分片，确保文档是最新版本。

## 如何选举Master节点

### Elasticsearch 的分布式原理

Elasticsearch 会对存储的数据进行切分，将数据划分到不同的分片上，同时每一个分片会保存多个副本，主要是为了保证分布式环境的高可用。在 Elasticsearch 中，节点是对等的，节点间会选取集群的 Master，由 Master 会负责集群状态信息的改变，并同步给其他节点。

Elasticsearch 的性能会不会很低：只有建立索引和类型需要经过 Master，数据的写入有一个简单的 Routing 规则，可以路由到集群中的任意节点，所以数据写入压力是分散在整个集群的。

### Elasticsearch 如何选举 Master

Elasticsearch 的选主是 ZenDiscovery 模块负责的，主要包含 Ping（节点之间通过这个RPC来发现彼此）和 Unicast（单播模块包含一个主机列表以控制哪些节点需要ping通）这两部分；

- 确认候选主节点的最少投票通过数量，elasticsearch.yml 设置的值 `discovery.zen.minimum_master_nodes`;
- 对所有候选 master 的节点（`node.master: true`）根据 nodeId 字典排序，每次选举每个节点都把自己所知道节点排一次序，然后选出第一个（第0位）节点，暂且认为它是master节点。
- 如果对某个节点的投票数达到阈值，并且该节点自己也选举自己，那这个节点就是master。否则重新选举一直到满足上述条件。

补充：master节点的职责主要包括集群、节点和索引的管理，不负责文档级别的管理；data节点可以关闭http功能。

### Elasticsearch是如何避免脑裂现象

（1）当集群中 master 候选节点数量不小于3个时（`node.master: true`），可以通过设置最少投票通过数量（`discovery.zen.minimum_master_nodes`），设置超过所有候选节点一半以上来解决脑裂问题，即设置为 `(N/2)+1`；

（2）当集群 master 候选节点 只有两个时，这种情况是不合理的，最好把另外一个`node.master`改成false。如果我们不改节点设置，还是套上面的`(N/2)+1`公式，此时`discovery.zen.minimum_master_nodes`应该设置为2。这就出现一个问题，两个master备选节点，只要有一个挂，就选不出master了

## 建立索引阶段性能提升方法

1. 使用 SSD 存储介质

2. 使用批量请求并调整其大小：每次批量数据 5–15 MB 大是个不错的起始点。

3. 如果你在做大批量导入，考虑通过设置 `index.number_of_replicas: 0` 关闭副本

4. 如果你的搜索结果不需要近实时的准确度，考虑把每个索引的 `index.refresh_interval` 改到30s

5. 段和合并：Elasticsearch 默认值是 20 MB/s。但如果用的是 SSD，可以考虑提高到 100–200 MB/s。如果你在做批量导入，完全不在意搜索，你可以彻底关掉合并限流。

6. 增加 `index.translog.flush_threshold_size` 设置，从默认的 512 MB 到更大一些的值，比如 1 GB

## 深度分页与滚动搜索scroll

**（1）深度分页：**

深度分页其实就是搜索的深浅度，比如第1页，第2页，第10页，第20页，是比较浅的；第10000页，第20000页就是很深了。搜索得太深，就会造成性能问题，会耗费内存和占用 cpu。而且 es 为了性能，他不支持超过一万条数据以上的分页查询。

那么如何解决深度分页带来的问题，我们应该避免深度分页操作（限制分页页数），比如最多只能提供 100 页的展示，从第 101 页开始就没了，毕竟用户也不会搜的那么深。

**（2）滚动搜索：**

一次性查询1万+数据，往往会造成性能影响，因为数据量太多了。这个时候可以使用滚动搜索，也就是 scroll。滚动搜索可以先查询出一些数据，然后再紧接着依次往下查询。

在第一次查询的时候会有一个滚动id，相当于一个锚标记 ，随后再次滚动搜索会需要上一次搜索滚动id，根据这个进行下一次的搜索请求。每次搜索都是基于一个历史的数据快照，查询数据的期间，如果有数据变更，那么和搜索是没有关系的。

## 参考

+ [ElasticSearch常见问题汇总](https://zhuanlan.zhihu.com/p/429104939)
+ [Elasticsearch 入门学习](https://zhuanlan.zhihu.com/p/104215274)
+ [说说你对ElasticSearch的理解](https://zhuanlan.zhihu.com/p/649898036)





