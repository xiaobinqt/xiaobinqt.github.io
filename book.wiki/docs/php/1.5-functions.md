---
weight: 5

bookFlatSection: true

bookCollapseSection: false

bookToc: true

title: "1.5 常用函数"
---

# 常用函数

## 字符串处理

1. strlen() - 返回字符串的长度。
2. strpos() - 查找字符串中的子字符串并返回其第一次出现的位置。
3. substr() - 返回字符串的一部分。
4. strtolower() - 将字符串转换为小写。
5. strtoupper() - 将字符串转换为大写。
6. str_replace() - 在字符串中替换指定的子字符串。
7. trim() - 去除字符串两端的空格或其他字符。
8. explode() - 将字符串拆分成数组，根据指定的分隔符。
9. implode() - 将数组元素连接成字符串，使用指定的分隔符。
10. ucfirst() - 将字符串的首字母转换为大写。
11. ucwords() - 将字符串中每个单词的首字母转换为大写。
12. strcmp() - 比较两个字符串。
13. strstr() - 查找字符串中的子字符串并返回其后的部分。
14. strrev() - 反转字符串。
15. htmlspecialchars() - 将特殊字符转换为HTML实体。
16. preg_match() - 使用正则表达式进行字符串匹配。
17. rtrim() - 去除字符串右侧的空格或其他字符。
18. ltrim() - 去除字符串左侧的空格或其他字符。
19. mb_strlen() - 返回多字节字符串的长度。
20. mb_substr() - 返回多字节字符串的一部分。


## 数组处理

1. count() - 返回数组中元素的数量。
2. array_push() - 将一个或多个元素添加到数组末尾。
3. array_pop() - 删除并返回数组的最后一个元素。
4. array_shift() - 删除并返回数组的第一个元素。
5. array_unshift() - 在数组开头添加一个或多个元素。
6. array_merge() - 合并一个或多个数组。
7. array_slice() - 返回数组的一部分。
8. array_reverse() - 反转数组。
9. in_array() - 检查数组中是否存在某个值。
10. array_keys() - 返回数组中的所有键名。
11. array_values() - 返回数组中所有的值。
12. array_search() - 在数组中搜索给定的值，并返回对应的键名。
13. array_unique() - 移除数组中的重复值。
14. array_filter() - 根据回调函数的条件过滤数组元素。
15. array_map() - 对数组的每个元素应用回调函数。
16. array_sum() - 返回数组中所有值的和。
17. array_splice() - 删除或替换数组中的元素，并可以插入新元素。
18. sort() - 对数组进行升序排序。
19. rsort() - 对数组进行降序排序。
20. array_rand() - 从数组中随机返回一个或多个键名。

## 其他

1. date() - 格式化日期和时间。
2. time() - 返回当前的Unix时间戳。
3. strtotime() - 将日期时间字符串解析为Unix时间戳。
4. include() - 在当前文件中包含并执行指定文件。
5. require() - 在当前文件中包含并执行指定文件，但出错时会产生致命错误。
6. fopen() - 打开文件或URL。
7. fclose() - 关闭文件句柄。
8. file_get_contents() - 将整个文件读入一个字符串。
9. file_put_contents() - 将一个字符串写入文件。
10. json_encode() - 将 PHP 值转换为 JSON 格式的字符串。
11. json_decode() - 将 JSON 格式的字符串转换为 PHP 值。
12. is_numeric() - 检测变量是否为数值或数值字符串。
13. empty() - 检测变量是否为空。
14. isset() - 检测变量是否已声明并且不为NULL。
15. filter_var() - 过滤变量，比如验证邮箱、URL等。
16. intval() - 将变量转换为整数类型。
17. floatval() - 将变量转换为浮点数类型。
18. is_array() - 检测变量是否为数组类型。
19. is_string() - 检测变量是否为字符串类型。
20. exit() 或 die() - 终止脚本的执行并输出一条消息。

