---
title: "JS运行机制"

date: 2022-03-18T15:09:13+08:00

lastmod: 2022-03-18T15:09:13+08:00

draft: false

author: "xiaobinqt"
description: ""
resources:

- name: ""
  src: ""

tags: ["js"]
categories: ["web"]
lightgallery: true

toc:
auto: false

math:
enable: true
---

## 执行模式

JS的执行模式是单线程的，当有多个任务时必须排队执行，优点是执行环境简单，缺点是性能低下，当有多个任务时，需要等待上一个任务执行完成才能执行下一个任务， 如果某个任务出现了死循环，那么就会导致程序崩溃。 所以JS出现了同步和异步的概念。

### 同步

后一个任务等待前一个任务结束，然后再执行，程序的执行顺序与任务的排列顺序是一致的。

### 异步

每一个任务有一个或多个回调函数（callback），前一个任务结束后，不是执行后一个任务，而是执行回调函数，后一个任务则是不等前一个任务结束就执行，所以程序的执行顺序与任务的排列顺序可能是不一致的。

## Event Loop

// TODO

## Promise

### 单个 promise

### 多个 promise

## async/await的用法和理解

async 函数是非常新的语法功能，在 ES7 中可用。

async 函数返回一个 Promise 对象，可以使用 then 方法添加回调函数。await 作为修饰符，只能放在 async 内部使用。 当函数执行的时候，一旦遇到 await
就会先返回，等到触发的异步操作完成，再接着执行函数体内后面的语句。

await 等待右侧表达式的结果。 如果等到的不是一个 promise 对象，那 await 表达式的运算结果就是它等到的东西。 如果它等到的是一个 promise 对象，它会阻塞后面的代码，等着 promise 对象
resolve，然后得到 resolve 的值，作为 await 表达式的运算结果。

```javascript
async function test() {
    let promise = new Promise(resolve => {
        setTimeout(() => resolve("test"), 2000);
    });
    await promise.then((ret) => {
        console.log(ret)
    })
    let test1Ret = await test1()
    console.log(test1Ret)
    console.log("test end...")
}

function test1() {
    return "test1_return"
}

test();
console.log('end')
```

![运行结果](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220318/77b8072751844d84a1f96272c46b7735.png?imageView2/0/interlace/1/q/50|imageslim ' ')

## 宏任务和微任务

// TODO

## 参考

+ [Javascript异步编程的4种方法](http://www.ruanyifeng.com/blog/2012/12/asynchronous%EF%BC%BFjavascript.html)
+ [JavaScript 运行机制详解：再谈Event Loop](https://www.ruanyifeng.com/blog/2014/10/event-loop.html)
+ [async 函数的含义和用法](http://www.ruanyifeng.com/blog/2015/05/async.html)
+ [你真的了解回调?](https://mp.weixin.qq.com/s?__biz=MzI4OTc3NDgzNQ==&mid=2247484695&idx=1&sn=57b4e00a6929784ae9c5026cc71f46ef)
+ [回调地狱](https://mp.weixin.qq.com/s?__biz=MzI4OTc3NDgzNQ==&mid=2247484700&idx=1&sn=0a840596519263dd8baa1e4a0f265151)