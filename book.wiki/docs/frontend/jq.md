---
weight: 2

bookFlatSection: true

bookCollapseSection: false

bookToc: true

title: "Jquery"
---

# Jquery

## 获取值

todo..

## base64 数据给前端使用

后端可以用 base64 把数据传给前端，前端直接用，特别是常见的：

- 图片
- 小文件
- 小段 JSON

比如**后端 PHP**：

```php
<?php
$data = [
    "s3_region" => "us-east-2",
    "s3_bucket" => "avator",
];
// 1. 转 JSON
$json = json_encode($data, JSON_UNESCAPED_UNICODE);

// 2. 再 base64 编码
$base64 = base64_encode($json);
?>
<input type="hidden" id="s3_config" value="<?= $base64 ?>">
```

JS 前端解码回来：

```javascript
const base64Str = $('#s3_config').val();
const jsonStr = atob(base64Str);   // base64 decode
const config = JSON.parse(jsonStr); // 解析 JSON

console.log(config.s3_region); // us-east-2
```

为什么用 base64？什么时候用？

| 用途           | 解释                           |
|:-------------|:-----------------------------|
| 避免 HTML 转义问题 | 里面即使有 `"`、`<`、`>` 都不会影响 HTML |
| 保证内容完整安全     | base64是纯字符串，不会破坏标签结构         |
| 小数据安全传递      | 一般几 KB 以内的数据可以这样做            |

### 注意事项 ⚡

- **大数据量不要 base64**：因为 base64 会比原数据大 **33% 左右**，太大就浪费带宽。
- **小段数据（JSON、短文本）非常合适**。
- **图片的话**，小图 base64 没问题，大图最好还是用 URL。

## 页面加载时就执行

如果想在 页面加载完成 时就用 **jQuery** 自动执行某些代码。
最常见的方法就是用 `$(document).ready()` 或 `$(function() {...})`。

### ✅ 最标准写法：

```javascript
$(document).ready(function () {
    // 页面加载完成后自动执行这里的代码
    console.log("页面加载完成，开始执行任务！");
    upload(2);  // 举个例子，直接执行你的 upload(2)
});
```

### ✅ 简写版（更常用）

```javascript
$(function () {
    console.log("页面加载完成！");
    upload(2);
});
```

页面里要先引入 jQuery：

  ```html

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  ```

（一般是放在 `<head>` 或 `<body>` 结尾）

- `$(function(){})` 和 `$(document).ready(function(){})` 是等价的，写哪个都行。

## 判断页面上是否有某个元素

在 jQuery 中判断页面上是否存在某个元素，通常有几种方法。可以使用 `.length` 属性来判断是否找到了匹配的元素。

```javascript
const input = $(`textarea[name="${lang}"]`);

if (input.length > 0) {
    console.log("元素存在");
    // 执行你需要的操作
} else {
    console.log("元素不存在");
    // 做其他处理
}
```

`input.length`: jQuery 选择器返回的是一个 jQuery 对象，它的 `.length` 属性表示匹配的元素数量。**如果 `.length` 大于 `0`，说明页面上存在该元素；否则，元素不存在**。

另一种方法：使用 `if (input)` 判断

```javascript
const input = $(`textarea[name="${lang}"]`);

if (input.length) {
    console.log("元素存在");
} else {
    console.log("元素不存在");
}
```

- **`input.length`** 判断返回的是元素集合的长度，`length > 0` 表示元素存在。
- `input` 本身是一个 jQuery 对象，通过 `.length` 可以快速判断是否找到了元素。










