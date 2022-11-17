# Go sync.Map 解读


<!-- author： xiaobinqt -->
<!-- email： xiaobinqt@163.com -->
<!-- https://xiaobinqt.github.io -->
<!-- https://www.xiaobinqt.cn -->

## 背景

项目中遇到了需要使用高并发的 map 的场景，众所周知 Go 官方的原生 map 是不支持并发读写的，直接并发的读写很容易触发 panic。

解决的办法有两个：

+ 自己配一把锁`sync.Mutex`，或者更加考究一点配一把读写锁`sync.RWMutex`。这种方案简约直接，但是缺点也明显，就是性能不会太高。
+ 使用 Go 语言在 2017 年发布的 Go 1.9 中正式加入了并发安全的字典类型`sync.Map`。

很显然，方案 2 是优雅且实用的。但是，为什么官方的`sync.Map`能够在 [lock free]^(无锁并发) 的前提下，保证足够高的性能？本文结合源码进行简单的分析。

## 核心思想＆架构

如果要保证并发的安全，最朴素的想法就是使用锁，但是这意味着要把一些并发的操作强制串行化，性能自然就会下降。

事实上，除了使用锁，还有一个办法，也可以达到类似并发安全的目的，就是原子操作`atomic`。

`sync.Map`的设计非常巧妙，充分利用了`atmoic`和`mutex`的配合。

### 核心思想

核心原则就是，尽量使用原子操作，最大程度上减少了锁的使用，从而接近了 lock free 的效果。

核心点：

- 使用了两个原生的 map 作为存储介质，分别是 [read map]^(只读字典) 和 [dirty map]^(脏字典)。


- 只读字典使用`atomic.Value`来承载，保证原子性和高性能；脏字典则需要用互斥锁来保护，保证了互斥。


- 只读字典和脏字典中的键值对集合并不是实时同步的，它们在某些时间段内可能会有不同。


- 无论是 read 还是 dirty，本质上都是`map[interface{}]*entry`类型，这里的 entry 其实就是 Map 的 value 的容器。


- entry 的本质，是一层封装，可以表示具体值的指针，也可以表示 key 已删除的状态（即逻辑假删除）。

通过这种设计，规避了原生 map 无法并发安全 delete 的问题，同时在变更某个键所对应的值的时候，就也可以使用原子操作了。

这里列一下 Map 的源码定义。篇幅问题，我去除了大量的英文原版注释，换成融合自身理解的直观解释。如果有需要可以结合原版的注释对比着看。

```
type Map struct {
	mu sync.Mutex

	// read contains .... 省略原版的注释
	// read map是被atomic包托管的，这意味着它本身Load是并发安全的（但是它的Store操作需要锁mu的保护）
	// read map中的entries可以安全地并发更新，但是对于expunged entry，在更新前需要经它unexpunge化并存入dirty
	//（这句话，在Store方法的第一种特殊情况中，使用e.unexpungeLocked处有所体现）
	read atomic.Value // readOnly

	// dirty contains .... 省略原版的注释
	// 关于dirty map必须要在锁mu的保护下，进行操作。它仅仅存储 non-expunged entries
	// 如果一个 expunged entries需要存入dirty，需要先进行unexpunged化处理
	// 如果dirty map是nil的，则对dirty map的写入之前，需要先根据read map对dirty map进行浅拷贝初始化
	dirty map[interface{}]*entry

	// misses counts .... 省略原版的注释
	// 每当读取的是时候，read中不存在，需要去dirty查看，miss自增，到一定程度会触发dirty=>read升级转储
	// 升级完毕之后，dirty置空 &miss清零 &read.amended置false
	misses int
}

// 这是一个被原子包atomic.Value托管了的结构，内部仍然是一个map[interface{}]*entry
// 以及一个amended标记位，如果为真，则说明dirty中存在新增的key，还没升级转储，不存在于read中
type readOnly struct {
	m       map[interface{}]*entry
	amended bool // true if the dirty map contains some key not in m.
}

// An entry is a slot in the map corresponding to a particular key.
// 这是一个容器，可以存储任意的东西，因为成员p是unsafe.Pointer(*interface{})
// sync.Map中的值都不是直接存入map的，都是在entry的包裹下存入的
type entry struct {
	// p points ....  省略原版的注释
	// entry的p可能的状态：
	// e.p == nil：entry已经被标记删除，不过此时还未经过read=>dirty重塑，此时可能仍然属于dirty（如果dirty非nil）
	// e.p == expunged：entry已经被标记删除，经过read=>dirty重塑，不属于dirty，仅仅属于read，下一次dirty=>read升级，会被彻底清理
	// e.p == 普通指针：此时entry是一个不同的存在状态，属于read，如果dirty非nil，也属于dirty
	p unsafe.Pointer // *interface{}
}

```

### 架构设计图

初看这个结构的设计，会觉得复杂，不理解为什么要设计成这样，这里画了一个图，力求更加直观的说明 read 和 dirty 之间的配合关系。

![设计架构图](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221025/3b41e0a3ca3443d0b1d8a2daba7aab8a.png '设计架构图')

[//]: # (![图片]&#40;https://mmbiz.qpic.cn/mmbiz_png/VY8SELNGe94AbDtkhBXlO1BKXJKXQl9Gs5O4nf1G2rRQnRbfk7ze7SUwsgJCHGQupcuQTLTNgjB9mNAl0mG2Tw/640&#41;)

架构的进一步解释说明：

- read map 由于是原子包托管，主要负责高性能，但是无法保证拥有全量的 key（因为对于新增 key，会首先加到 dirty 中），所以 read 某种程度上，类似于一个 key 的快照。


- dirty map 拥有全量的 key，当 Store 操作要新增一个之前不存在的 key 的时候，预先是增加自 dirty 中的。


- 在查找指定的 key 的时候，总会先去只读字典中寻找，并不需要锁定互斥锁。只有当 read 中没有，但 dirty 中可能会有这个 key 的时候，才会在锁的保护下去访问 dirty。


- 在存储键值对的时候，只要 read 中已存有这个 key，并且该键值对未被标记为`expunged`，就会把新值存到里面并直接返回，这种情况下也不需要用到锁。


- expunged 和 nil，都表示标记删除，但是它们是有区别的，简单说 expunged 是 read 独有的，而 nil 则是 read 和 dirty 共有的，具体这么设计的原因，最后统一总结。


- read 和 map 的关系，是一直在动态变化的，可能存在重叠，也可能是某某一方为空；重叠的公共部分，由分为两种情况，nil 和 normal，它们分别的意义，会在最后统一总结。


- read 和 dirty 之间是会互相转换的，在 dirty 中查找 key 对次数足够多的时候，`sync.Map`会把 dirty 直接作为 read，即触发 `dirty=>read`升级。同时在某些情况，也会出现`read=>dirty`的重塑，具体方式和这么设计的原因，最后详述。

## 源码细节梳理

通过上面的分析，可以对`sync.Map`有一个初步的整体认知，这里再列出 CURD 几个关键操作的源码，进一步加深理解。同样的由于篇幅原因，我去除了大段冗长的英文注释，换成了提炼之后更加通俗的理解，有需要可以对比原文注释。

### Store操作（对应C/U）

```
// Store sets the value for a key.
func (m *Map) Store(key, value interface{}) {
	// 首先把readonly字段原子地取出来
	// 如果key在readonly里面，则先取出key对应的entry，然后尝试对这个entry存入value的指针
	read, _ := m.read.Load().(readOnly)
	if e, ok := read.m[key]; ok && e.tryStore(&value) {
		return
	}

	// 如果readonly里面不存在key或者是对应的key是被擦除掉了的，则继续。。。
	m.mu.Lock() // 上锁

	// 锁的惯用模式：再次检查readonly，防止在上锁前的时间缝隙出现存储
	read, _ = m.read.Load().(readOnly)
	if e, ok := read.m[key]; ok {
		// 这里有两种情况：
		// 1. 上面的时间缝隙里面，出现了key的存储过程（可能是normal值，也可能是expunge值）
		//    此时先校验e.p，如果是普通值，说明read和dirty里都有相同的entry，则直接设置entry
		//    如果是expunge值，则说明dirty里面已经不存在key了，需要先在dirty里面种上key，然后设置entry
		// 2. 本来read里面就存在，只不过对应的entry是expunge的状态
		//    这种情况和上面的擦除情况一样，说明dirty里面已经不存在key了，需要先在dirty里面种上key，然后设置entry
		if e.unexpungeLocked() {
			// The entry was previously expunged, which implies that there is a
			// non-nil dirty map and this entry is not in it.
			m.dirty[key] = e
		}
		e.storeLocked(&value) // 将value存入容器e
	} else if e, ok := m.dirty[key]; ok {
		// readonly里面不存在，则查看dirty里面是否存在
		// 如果dirty里面存在，则直接设置dirty的对应key
		e.storeLocked(&value)
	} else {
		// dirty里面也不存在（或者dirty为nil），则应该先设置在ditry里面
		// 此时要检查read.amended，如果为假（标识dirty中没有自己独有的key or 两者均是初始化状态）
		// 此时要在dirty里面设置新的key，需要确保dirty是初始化的且需要设置amended为true（表示自此dirty多出了一些独有key）
		if !read.amended {
			// We're adding the first new key to the dirty map.
			// Make sure it is allocated and mark the read-only map as incomplete.
			m.dirtyLocked()
			m.read.Store(readOnly{m: read.m, amended: true})
		}
		m.dirty[key] = newEntry(value)
	}

	// 解锁
	m.mu.Unlock()
}

// 这是一个自旋乐观锁：只有key是非expunged的情况下，会得到set操作
func (e *entry) tryStore(i *interface{}) bool {
	for {
		p := atomic.LoadPointer(&e.p)
		// 如果p是expunged就不可以了set了
		// 因为expunged状态是read独有的，这种情况下说明这个key已经删除（并且发生过了read=>dirty重塑过）了
		// 此时要新增只能在dirty中，不能在read中
		if p == expunged {
			return false
		}
		// 如果非expunged，则说明是normal的entry或者nil的entry，可以直接替换
		if atomic.CompareAndSwapPointer(&e.p, p, unsafe.Pointer(i)) {
			return true
		}
	}
}

// 利用了go的CAS，如果e.p是 expunged，则将e.p置为空，从而保证她是read和dirty共有的
func (e *entry) unexpungeLocked() (wasExpunged bool) {
	return atomic.CompareAndSwapPointer(&e.p, expunged, nil)
}

// 真正的set操作，从这里也可以看出来2点：1是set是原子的 2是封装的过程
func (e *entry) storeLocked(i *interface{}) {
	atomic.StorePointer(&e.p, unsafe.Pointer(i))
}

// 利用read重塑dirty！
// 如果dirty为nil，则利用当前的read来初始化dirty（包括read本身也为空的情况）
// 此函数是在锁的保护下进行，所以不用担心出现不一致
func (m *Map) dirtyLocked() {
	if m.dirty != nil {
		return
	}
	// 经过这么一轮操作:
	// dirty里面存储了全部的非expunged的entry
	// read里面存储了dirty的全集，以及所有expunged的entry
	// 且read中不存在e.p == nil的entry（已经被转成了expunged）
	read, _ := m.read.Load().(readOnly)
	m.dirty = make(map[interface{}]*entry, len(read.m))
	for k, e := range read.m {
		if !e.tryExpungeLocked() { // 只有非擦除的key，能够重塑到dirty里面
			m.dirty[k] = e
		}
	}
}

// 利用乐观自旋锁，
// 如果e.p是nil，尽量将e.p置为expunged
// 返回最终e.p是否是expunged
func (e *entry) tryExpungeLocked() (isExpunged bool) {
	p := atomic.LoadPointer(&e.p)
	for p == nil {
		if atomic.CompareAndSwapPointer(&e.p, nil, expunged) {
			return true
		}
		p = atomic.LoadPointer(&e.p)
	}
	return p == expunged
}

```

### Store操作（对应R）

```

func (m *Map) Load(key interface{}) (value interface{}, ok bool) {
   // 把readonly字段原子地取出来
   read, _ := m.read.Load().(readOnly)
   e, ok := read.m[key]

   // 如果readonly没找到，且dirty包含了read没有的key，则尝试去dirty里面找
   if !ok && read.amended {
      m.mu.Lock()
      // 锁的惯用套路
      read, _ = m.read.Load().(readOnly)
      e, ok = read.m[key]
      if !ok && read.amended {
         e, ok = m.dirty[key]
         // Regardless of ... 省略英文
         // 记录miss次数，并在满足阈值后，触发dirty=>map的升级
         m.missLocked()
      }
      m.mu.Unlock()
   }

   // readonly和dirty的key列表，都没找到，返回nil
   if !ok {
      return nil, false
   }

   // 找到了对应entry，随即取出对应的值
   return e.load()
}

// 自增miss计数器
// 如果增加到一定程度，dirty会升级成为readonly（dirty自身清空 & read.amended置为false）
func (m *Map) missLocked() {
   m.misses++
   if m.misses < len(m.dirty) {
      return
   }
   // 直接用dirty覆盖到了read上（那也就是意味着dirty的值是必然是read的父集合，当然这不包括read中的expunged entry）
   m.read.Store(readOnly{m: m.dirty}) // 这里有一个隐含操作，read.amended再次变成false
   m.dirty = nil
   m.misses = 0
}

// entry是一个容器，从entry里面取出实际存储的值（以指针提取的方式）
func (e *entry) load() (value interface{}, ok bool) {
   p := atomic.LoadPointer(&e.p)
   if p == nil || p == expunged {
      return nil, false
   }
   return *(*interface{})(p), true
}

```

### Delete操作（对应D）

```

// Delete deletes the value for a key.
func (m *Map) Delete(key interface{}) {
   m.LoadAndDelete(key)
}

// 删除的逻辑和Load的逻辑，基本上是一致的
func (m *Map) LoadAndDelete(key interface{}) (value interface{}, loaded bool) {
   read, _ := m.read.Load().(readOnly)
   e, ok := read.m[key]
   if !ok && read.amended {
      m.mu.Lock()
      read, _ = m.read.Load().(readOnly)
      e, ok = read.m[key]
      if !ok && read.amended {
         e, ok = m.dirty[key]
         delete(m.dirty, key)
         // Regardless of ...省略
         m.missLocked()
      }
      m.mu.Unlock()
   }
   if ok {
      return e.delete()
   }
   return nil, false
}

// 如果e.p == expunged 或者nil，则返回false
// 否则，设置e.p = nil，返回删除的值得指针
func (e *entry) delete() (value interface{}, ok bool) {
   for {
      p := atomic.LoadPointer(&e.p)
      if p == nil || p == expunged {
         return nil, false
      }
      if atomic.CompareAndSwapPointer(&e.p, p, nil) {
         return *(*interface{})(p), true
      }
   }
}
```

## 整体思考

第一次读 Map 的源码，会觉得很晦涩，虽然整体思路是明确的，但是细节却很多，困惑于为什么做这样的设计，多读几遍之后，很多问题能够略窥门径。这里列出一些开始觉得困惑的问题：

### dirty 和 read 互转，分别在什么样的时机下会进行？

- `dirty=>read`：随着 load 的 miss 不断自增，达到阈值后触发升级转储（完毕之后，dirty 置空`&miss`清零`&read.amended`置false）


- `read=>dirty`
  ：当有 read 中不存在的新 key 需要增加且 read 和 dirty 一致的时候，触发重塑，且`read.amended`置 true（然后再在 dirty 新增）。重塑的过程，会将 nil 状态的 entry，全部挤压到 expunged 状态中，同时将非 expunged 的 entry 浅拷贝到 dirty 中，这样可以避免 read 的 key 无限的膨胀（存在大量逻辑删除的 key）。最终，在 dirty 再次升级为 read 的时候，这些逻辑删除的 key 就可以一次性丢弃释放了（因为是直接覆盖上去）

![read=>dirty](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221025/e8837d7eda904db586f5e78b23a69ef2.png 'read=>dirty')

[//]: # (![图片]&#40;https://mmbiz.qpic.cn/mmbiz_png/VY8SELNGe94AbDtkhBXlO1BKXJKXQl9GojOb0gy17kB2fq1tDh3XUF2dstwXtk9bicGOTwR9qmrP2h2qKzsaWMA/640&#41;)

### read 从何而来，存在的意义又是什么？

+ read 是由 dirty 升级而来，是利用了`atomic.Store`一次性覆盖，而不是一点点的 set 操作出来的。所以，read 更像是一个快照，read 中 key 的集合不能被改变（注意，这里说的 read 的 key 不可改变，不代表指定的 key 的 value 不可改变，value 是可以通过原子`CAS`
  来进行更改的），所以其中的键的集合有时候可能是不全的。

+ 相反，脏字典中的键值对集合总是完全的，但是其中不会包含expunged的键值对。


+ read 的存在价值，在于加速读性能（通过原子操作避免了锁）

### entry 的 p 可能的状态，有哪些？

- `e.p==nil`：entry 已经被标记删除，不过此时还未经过`read=>dirty`重塑，此时可能仍然属于 dirty（如果 dirty 非 nil）


- `e.p==expunged`：entry 已经被标记删除，经过`read=>dirty`重塑，不属于 dirty，仅仅属于 read，下一次`dirty=>read`
  升级，会被彻底清理（因为升级的操作是直接覆盖，read 中的 expunged 会被自动释放回收）


- `e.p==普通指针`：此时 entry 是一个普通的存在状态，属于 read，如果 dirty 非 nil，也属于 dirty。对应架构图中的 normal 状态。

### 删除操作的细节，`e.p`到底是设置成了 nil 还是 expunged？

- 如果 key 不在 read 中，但是在 dirty 中，则直接 delete。


- 如果 key 在 read 中，则逻辑删除，`e.p`赋值为 nil(后续在重塑的时候，nil 会变成 expunged )

### 什么时候 e.p 由 nil 变成 expunged？

- `read=>dirty`重塑的时候，此时 read 中仍然是 nil 的，会变成 expunged，表示这部分 key 等待被最终丢弃（expunged 是最终态，等待被丢弃，除非又出现了重新 store 的情况）


- 最终丢弃的时机：就是`dirty=>read`升级的时候，dirty 的直接粗暴覆盖，会使得 read 中的所有成员都被丢弃，包括 expunged。

### 既然 nil 也表示标记删除，那么再设计出一个 expunged 的意义是什么？

expunged 是有存在意义的，它作为删除的最终状态（待释放），这样 nil 就可以作为一种中间状态。如果仅仅使用 nil，那么，在`read=>dirty`重塑的时候，可能会出现如下的情况：

- 如果 nil 在 read 浅拷贝至 dirty 的时候仍然保留 entry 的指针（即拷贝完成后，对应键值下 read 和 dirty 中都有对应键下 entry e 的指针，且`e.p=nil`）那么之后在`dirty=>read`升级 key 的时候对应 entry 的指针仍然会保留。那么最终；的合集会越来越大，存在大量 nil 的状态，永远无法得到清理的机会。


- 如果 nil 在 read 浅拷贝时不进入 dirty，那么之后 store 某个 Key 键的时候，可能会出现 read 和 dirty 不同步的情况，即此时 read 中包含 dirty 不包含的键，那么之后用 dirty 替换 read 的时候就会出现数据丢失的问题。


- 如果 nil 在 read 浅拷贝时直接把 read 中对应键删除（从而避免了不同步的问题），但这又必须对 read 加锁，违背了 read 读写不加锁的初衷。

综上，为了保证 read 作为快照的性质（不能单独删除或新增key），同时要避免 Map 中 nil 的 key 不断膨胀等多个前提要求，才设计成了 expungd 的状态。

### 对于一个 entry，从生到死的状态机图

![entry 从生到死的状态机图](https://cdn.xiaobinqt.cn/xiaobinqt.io/20221025/0e888b76b2f14ecc89735f7d0d314eae.png 'entry 从生到死的状态机图')

[//]: # (![图片]&#40;https://mmbiz.qpic.cn/mmbiz_png/VY8SELNGe94AbDtkhBXlO1BKXJKXQl9GWUOhA9Erx0DrC7kveAumicawYmnwwbcWo1IeUpYxkDZ2sv5XiaAf8pPw/640&#41;)

### 注释中关于 slow path 和 fast path 的解释

- 慢路径其实就是经过了锁的代码路径。

- 快路径就是不经过锁的。

## 总结

`sync.Map`的源码并不长，但是里面的很多细节都非常的考究，比如对于原子和锁的使用、利用状态机的变化标记来代替 map 的 delete 从而提高性能和安全性等等。

## 参考

+ [不得不知道的Golang之sync.Map解读！](https://view.inews.qq.com/k/20220613A08UDG00)
