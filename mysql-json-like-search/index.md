# 记一次 MySQL 8.0 JSON 查询


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

有 2 张表，一张 tag 表，主要字段有 id，name。一张 channel 表，有个 tags 字段，存 tag 表中 id，如：`[1,5]`。

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231012/972fed7bb89b4b57824d8ac62c4f226e.png 'tags')

现在的需求是，通过 channel 表可以支持模糊搜索 tag 的 name，比如 tag 表中的数据如下：

![](https://cdn.xiaobinqt.cn/xiaobinqt.io/20231012/753d023454524eb58b26a043e24c59ef.png 'tag')

channel 表中的某条数据的 tags 字段的值是 `[5,6]`，那我就可以通过搜索 `测试系统` 找到这条 channel 数据。

首先，可以使用 JSON 函数来解析 `tags` 列，然后再连接 `tag` 表以匹配 `id`。以下是一个示例 SQL 查询：

```sql
SELECT c.*
FROM channel c
         INNER JOIN tag t ON JSON_CONTAINS(c.tags, CAST(t.id AS JSON))
WHERE t.name LIKE '%your_search_query%';
```

这个查询的步骤是：

1. `FROM channel c`：从 `channel` 表中选择数据。
2. `INNER JOIN tag t ON JSON_CONTAINS(c.tags, CAST(t.id AS JSON))`：将 `channel` 表与 `tag` 表连接，其中 `JSON_CONTAINS` 用于检查 `tag` 是否在 `channel` 的 JSON 数组中。
3. `WHERE t.name LIKE '%your_search_query%'`：在连接后的结果中，使用 `LIKE` 子句来执行模糊匹配。

在上面的查询中，可以将 `%your_search_query%` 替换为想搜索的标签名称的部分。这将返回包含匹配的 `tag` 名称的结果集。

当在 SQL 中处理 JSON 数据时，可能需要将数据转换为 JSON 类型以进行比较或操作。在查询中，`JSON_CONTAINS(c.tags, CAST(t.id AS JSON))` 是一个用于检查 JSON 数组中是否包含特定值的 SQL 表达式。

以下是对这个表达式的详细解释：

1. **CAST(t.id AS JSON)**：这部分将 `t.id` 转换为 JSON 数据类型。在 SQL 中，`CAST` 函数用于将一个数据类型转换为另一个数据类型。在这里，`t.id` 是整数类型，通过 `CAST(t.id AS JSON)`，它被显式地转换为 JSON 类型。这是因为 `c.tags` 是一个 JSON 数据类型，所以需要确保进行比较的值也是 JSON 类型。

2. **JSON_CONTAINS(c.tags, CAST(t.id AS JSON))**：这是主要的比较部分。`JSON_CONTAINS` 函数用于检查一个 JSON 数组（在这里是 `c.tags`）是否包含特定值（在这里是 `t.id` 的 JSON 表示）。如果 `c.tags` 包含 `t.id` 的 JSON 表示，它将返回 true；否则，返回 false。这就允许查找 `channel` 表中具有特定 `tag` 的记录。

再用一个示例来解释这个过程：

假设 `channel` 表的某一行的 `tags` 列中包含 JSON 数组 `[1, 3, 5]`，想查找所有包含 `tag` 表中 `id` 为 3 的记录。

- `CAST(t.id AS JSON)` 将 `t.id`（3）转换为 JSON 数据类型，变成 `3`。
- `JSON_CONTAINS(c.tags, 3)` 将检查 `tags` 列中是否包含值为 3 的元素。
- 因为 `[1, 3, 5]` 包含值 3，所以这个表达式将返回 true。

这就是如何使用 `CAST` 函数和 `JSON_CONTAINS` 函数来进行 JSON 数据的比较和查询。在这个例子中，它允许在 `channel` 表中查找包含特定 `tag` 的记录。









