---
weight: 8

bookFlatSection: true

bookCollapseSection: false

bookToc: true

title: "Shell"
---

# Shell

shell 是外壳的意思，就是操作系统的外壳。我们可以通过 shell 命令来操作和控制操作系统，比如 Linux 中的 Shell 命令就包括 ls、cd、pwd 等等。总结来说，Shell 是一个命令解释器，它通过接受用户输入的 Shell 命令来启动、暂停、停止程序的运行或对计算机进行控制。

shell 是一个应用程序，它连接了用户和 Linux 内核，让用户能够更加高效、安全、低成本地使用 Linux 内核，这就是 Shell 的本质。

**shell 本身并不是内核的一部分，它只是站在内核的基础上编写的一个应用程序**。

那么什么是 shell 脚本呢？

shell 脚本就是由 Shell 命令组成的执行文件，将一些命令整合到一个文件中，进行处理业务逻辑，脚本不用编译即可运行。

shell 脚本中最重要的就是对 shell 命令的使用与组合，在使用 shell 脚本支持的一些语言特性，完成想要的功能。

## 注释

"#" 开头的就是注释，被编译器忽略

单行注释： #

多行注释：

```shell
: <<'COMMENT'
这是多行注释的第一行
第二行
第三行
COMMENT

a=1
```

## 变量

### 变量类型

运行 shell 时，会同时存在三种变量：

- 局部变量：局部变量在脚本或命令中定义，仅在当前 shell 实例中有效，其他 shell 启动的程序不能访问局部变量。
- 环境变量：所有的程序，包括 shell 启动的程序，都能访问环境变量，有些程序需要环境变量来保证其正常运行。必要的时候 shell 脚本也可以定义环境变量。
- shell 变量：shell 变量是由 shell 程序设置的特殊变量。shell变量中有一部分是环境变量，有一部分是局部变量，这些变量保证了 shell 的正常运行

### 变量操作

创建普通变量： `name="test"`，**=两边不可有空格**。

创建只可函数体中使用的局部变量：`local name="test"`，使用 local 修饰的变量在函数体外无法访问，并且 local 只能在函数体内使用。

使用变量： `echo $name` 或者 `echo ${name}`，**推荐使用大括号版**。

变量重新赋值： `name="new_test"`，将原值覆盖。

只读变量： `name="only_read"` -> `readonly name`。使用 readonly 标识后的变量，不可被修改。

删除变量：`unset name;`，删除之后不可访问，**删除不掉只读变量**。

### 字符串变量

#### 单引号

单引号变量`var='test'` ，只能原样输出，变量无效。

单引号中不能出现一个单独的单引号，转义也不可以

#### 双引号

双引号变量`var="my name is ${name}"`，变量有效，可出现转义符。

#### 拼接字符串

中间无任何+，之类的字符

`name="this is"" my name"`; `name="this is my name"`; `name='this''is''my name'` 等效

![](https://cdn.xiaobinqt.cn//xiaobinqt.io/20250429/ab2044b71fef4e258281d7da97e9985a.png)

#### 获取字符串长度

在`${}`中使用`#`获取长度

```shell
name="test";
echo ${#name}; # 输出为4
```

#### 提取子字符串

`1:4` 从第2个开始 往后截取 3 个字符

`::4` 从第一个字符开始 往后截取4个字符

```shell
name="this is my name";
echo ${name:1:4} #输出 his
echo ${name::4} #输出 this
```

![](https://cdn.xiaobinqt.cn//xiaobinqt.io/20250429/3548b396439341ceaee8ab309b4a2a30.png)

## 数组

bash **只支持**一维数组，不支持多维数组

定义数组：`array_name=(li wang xiang zhang)`。小括号做边界、使用空格分离。

单独定义数组的元素： `array_para[0]="w"`; `array_para[3]="s"`。定义时下标不连续也可以。

赋值数组元素：`array_name[0]="zhao"`;

### 获取数组元素

```shell
array_name[0]="li"
array_name[3]="zhang"
echo ${array_name[0]} # 输出"li"
echo ${array_name[1]} # 输出" "
echo ${array_name[3]} # 输出"zhang"
echo ${array_name[@]} # 输出"li zhang" 输出数组所有元素，没有元素的下标省略
```

取得元素个数：`${#array_name[@]}` 或者 `${#array_name}`

取得单个元素长度：`${#array_name[1]}`

![](https://cdn.xiaobinqt.cn//xiaobinqt.io/20250429/af50b93bdcf84acda5f1af1df9db2765.png)

## 参数传递

### 获取参数值

- $0 ： 固定，代表执行的文件名
- $1 ： 代表传入的第1个参数
- $n ： 代表传入的第n个参数
- $#：参数个数
- $\*： 以一个单字符串显示所有向脚本传递的参数。如 "$*" 用「"」括起来的情况、以 "$1 $2 … $n" 的形式输出所有参数
- $@：与 $* 相同，但是使用时加引号，并在引号中返回每个参数。
- $\$：脚本运行的当前进程号
- $！：后台运行的最后一个进程的ID
- $?： 显示最后命令的退出状态。0 表示没有错误，其他任何值表明有错误。

$* 与 $@ 区别

相同点：都是引用所有参数。

不同点：只有在双引号中体现出来。假设在脚本运行时写了三个参数 1、2、3，，则 "*" 等价于 "1 2 3"（传递了一个参数），而 "@" 等价于 "1" "2" "3"（传递了三个参数）。

## 运算符

### 算数运算

\+ 、-、*、\ ： 乘号前必须加 \ 进行转义才可以进行乘法运算

### 加法运算

```shell
  val=`expr 2 + 2` #（使用linux命令expr进行辅助运算）
  val=$[2+2] #（4个空格不是必要的，不同于条件判断）
  val2=$((2+2))
```

![](https://cdn.xiaobinqt.cn//xiaobinqt.io/20250429/b13b8e0504434c0a987d7f90ecd2a8c0.png)

### 数字关系运算符

关系运算符只支持数字，不支持字符串，**除非**字符串的值是数字。 下面假定变量 a 为 10，变量 b 为 20

- eq ：(equal) 检测两个数是否相等，相等返回 true。 [ $a -eq $b ] 返回 false。
- ne： (not equal) 检测两个数是否不相等，不相等返回 true。 [ $a -ne $b ] 返回 true。
- gt： (greater than) 检测左边的数是否大于右边的，如果是，则返回 true。 [ $a -gt $b ] 返回 false。
- lt： (less than) 检测左边的数是否小于右边的，如果是，则返回 true。 [ $a -lt $b ] 返回 true。
- ge： (greater or equal) 检测左边的数是否大于等于右边的，如果是，则返回 true。 [ $a -ge $b ] 返回 false。
- le：(less or equal) 检测左边的数是否小于等于右边的，如果是，则返回 true。 [ $a -le $b ] 返回 true。

### 字符串运算符

下表列出了常用的字符串运算符，假定变量 a 为 "abc"，变量 b 为 "efg"：

- `=` ：检测两个字符串是否相等，相等返回 true。 `[ $a = $b ]` 返回 false。
- `!=` ：检测两个字符串是否相等，不相等返回 true。 `[ $a != $b ]` 返回 true。
- `-z` ：检测字符串长度是否为 0，为 0 返回 true。 `[ -z $a ]` 返回 false。
- `-n` ：检测字符串长度是否为 0，不为 0 返回 true。 `[ -n "$a" ]` 返回 true。
- `$`：检测字符串是否为空，不为空返回 true。 `[ $a ]` 返回 true。

### 布尔运算符

下面列出了常用的布尔运算符，假定变量 a 为 10，变量 b 为 20：

- `!` ：非运算，表达式为 true 则返回 false，否则返回 true。 `[ ! false ]` 返回 true。
- `-o` ：或运算，有一个表达式为 true 则返回 true。 `[ $a -lt 20 -o $b -gt 100 ]` 返回 true。
- `-a` ：与运算，两个表达式都为 true 才返回 true。 `[ $a -lt 20 -a $b -gt 100 ]` 返回 false。

### 逻辑运算符

假定变量 a 为 10，变量 b 为 20:

- && ：逻辑的 AND `[ $a -lt 100 && $b -gt 100 ]` 返回 false
- || ：逻辑的 OR `[ $a -lt 100 || $b -gt 100 ]` 返回 true

### 文件运算符

- `-b file` ：检测文件是否是块设备文件，如果是，则返回 true。 `[ -b $file ]` 返回 false。
- `-c file` ：检测文件是否是字符设备文件，如果是，则返回 true。 `[ -c $file ]` 返回 false。
- `-d file` ：检测文件是否是目录，如果是，则返回 true。 `[ -d $file ]` 返回 false。
- `-f file` ：检测文件是否是普通文件（既不是目录，也不是设备文件），如果是，则返回 true。 `[ -f $file ]` 返回 true。
- `-g file` ：检测文件是否设置了 SGID 位，如果是，则返回 true。 `[ -g $file ]` 返回 false。
- `-k file` ：检测文件是否设置了粘着位(Sticky Bit)，如果是，则返回 true。 `[ -k $file ]` 返回 false。
- `-p file` ：检测文件是否是有名管道，如果是，则返回 true。 `[ -p $file ]` 返回 false。
- `-u file` ：检测文件是否设置了 SUID 位，如果是，则返回 true。 `[ -u $file ]` 返回 false。
- `-r file` ：检测文件是否可读，如果是，则返回 true。 `[ -r $file ]` 返回 true。
- `-w file` ：检测文件是否可写，如果是，则返回 true。 `[ -w $file ]` 返回 true。
- `-x file` ：检测文件是否可执行，如果是，则返回 true。 `[ -x $file ]` 返回 true。
- `-s file` ：检测文件是否为空（文件大小是否大于0），不为空返回 true。 `[ -s $file ]` 返回 true。
- `-e file` ：检测文件（包括目录）是否存在，如果是，则返回 true。 `[ -e $file ]` 返回 true。

## 执行相关

### 命令替换

命令替换与变量替换差不多，都是用来重组命令行的，先完成引号里的命令行，然后将其结果替换出来，再重组成新的命令行。

执行命令：

`ls /etc` ： 反引号，**所有的 unix 系统都支持**

$(ls /etc) ： $+()，部分 unix 系统不支持。

多个嵌套使用时，从内向外执行 `for file in /etc` 或 `for file in $(ls /etc)` 循环中使用

`dirname $0` 获取脚本文件所在的目录

```shell
path=$(cd `dirname $0`;pwd)
```

获取脚本当前所在目录，并且执行 cd 命令到达该目录，使用 pwd 获取路径并赋值到 path 变量。

![](https://cdn.xiaobinqt.cn//xiaobinqt.io/20250429/ee32c2c25147421f95e59b5ccc747c4d.png)

## 算术运算

$[] : 加减乘除，不必添加空格。

$(()) ：加减乘除等，不必添加空格

## 逻辑判断

- \[ \] ： 中括号旁边和运算符两边**必须**添加空格 （可以使用，不推荐）
- [[ ]]：中括号旁边和运算符两边**必须**添加空格 （字符串验证时，推荐使用）
- (()) ： 中括号旁边和运算符两边**必须**添加空格 （数字验证时，推荐使用）
- [[]] 和 (()) 分别是 [ ] 的针对数学比较表达式和字符串表达式的加强版。

使用 [[ ... ]] 条件判断结构，而不是 [ ... ]，能够防止脚本中的许多逻辑错误。

比如，&&、||、< 和 > 操作符能够正常存在于 [[ ]] 条件判断结构中，但是如果出现在 [ ] 结构中的话，会报错。

比如可以直接使用 `if [[ $a != 1 && $a != 2 ]]`, 如果不使用双括号, 则为 `if [ $a -ne 1] && [ $a != 2 ]` 或者 `if [ $a -ne 1 -a $a != 2 ]`。

[[ ]] 中增加模式匹配特效；

(( )) 不需要再将表达式里面的大小于符号转义，除了可以使用标准的数学运算符外，还增加了以下符号

![](https://cdn.xiaobinqt.cn//xiaobinqt.io/20250429/aba9dba5b16e43089fb60a10497288a0.png)

## 输出

### echo

仅用于字符串的输出，没有使用 printf 作为输出的移植性好，建议使用 printf

### printf

printf 不会像 echo 自动添加换行符，可以手动添加 \n，**无大括号**，直接以空格分隔。

格式：`printf format-string [arguments...]` 其中（format-string: 格式控制字符串、arguments: 参数列表）

案例：`printf "%-10s %-8s %-4.2f\n" 郭靖 男 66.1234`

![](https://cdn.xiaobinqt.cn//xiaobinqt.io/20250429/4e8e2add4f7e403382d85ef204046856.png)

%s %c %d %f 都是格式替代符

- d：Decimal 十进制整数，对应位置参数必须是十进制整数，否则报错。
- s：String 字符串，对应位置参数必须是字符串或者字符型，否则报错。
- c：Char 字符，对应位置参数必须是字符串或者字符型，否则报错。
- f：Float 浮点，对应位置参数必须是数字型 否则报错。
- %-10s ： 指一个宽度为 10 个字符（-表示左对齐，没有则表示右对齐），任何字符都会被显示在 10 个字符宽的字符内，如果不足则自动以空格填充，超过也会将内容全部显示出来。
- %-4.2f ：指格式化为小数，宽度为 4 个字符，其中 `.2` 指保留 2 位小数。

## 转义符

- \a ：警告字符，通常为 ASCII 的 BEL 字符
- \b ：后退
- \c ：抑制（不显示）输出结果中任何结尾的换行字符（只在%b格式指示符控制下的参数字符串中有效），而且，任何留在参数里的字符、任何接下来的参数以及任何留在格式字符串中的字符，都被忽略
- \f ：换页（formfeed）
- \n ：换行
- \r ：回车（Carriage return）
- \t ：水平制表符
- \v ：垂直制表符
- \ ：一个字面上的反斜杠字符
- \ddd ：表示 1 到 3 位数八进制值的字符。仅在格式字符串中有效
- \0ddd ：表示 1 到 3 位的八进制值字符

## 流程控制

和 Java、PHP 等语言不一样，shell 的流程控制不可为空，即 if 或者 else 的大括号中无任何语句

### if else

```shell
if condition then command1 command2 ... commandN fi

if condition then command1 command2 ... commandN else command fi

if condition1 then command1 elif condition2 then command2 else commandN fi

```

### for

```shell
for var in item1 item2 ... itemN do command1 command2 ... commandN done
```

### while

while condition

```shell
while condition do command done
```

while 无限循环

```shell
while : do command done
```

until

until 循环执行一系列命令直至条件为 true 时停止。 until 循环与 while 循环在处理方式上刚好相反。

```shell
until condition do command done
```

### case

case 语句为多选择语句。可以用 case 语句匹配一个值与一个模式，如果匹配成功，执行相匹配的命令。

case 需要一个 esac，就是 case 反过来，作为结束标记，每个 case 分支用右圆括号，用两个分号表示 break，其中 “;;” 不是跳出循环，是不在去匹配下面的模式。

case语句格式如下：

```shell
case 值 in 模式1) command1 command2 ... commandN ;; 模式2） command1 command2 ... commandN ;; esac
```

### 跳出循环

break ：跳出总循环

continue：跳出当前循环，继续下一次循环

## 定义函数

可以带 `function fun()` 定义，也可以直接 `fun()` 定义,不带任何参数。

函数定义

```shell
[ function ] funname() { action; [return int;] }
```

### 参数传递

调用函数: fun_name 2 3 4

函数中使用和 shell 取用函数相同 $n $# $* $? 或者加上 {}

```shell
funWithParam() {
    echo "第一个参数为 $1 !"
    echo "第二个参数为 $2 !"
    echo "第十个参数为 $10 !"
    echo "第十个参数为 ${10} !"
    echo "第十一个参数为 ${11} !"
    echo "参数总数有 $# 个!"
    echo "作为一个字符串输出所有参数 $* !"
}

funWithParam 1 2 3 4 5 6 7 8 9 34 73

echo $? # 判断执行是否成功
```

> Braces are required for positionals over 9, e.g. ${10}.

![](https://cdn.xiaobinqt.cn//xiaobinqt.io/20250430/d2f1552e9d574d0da4c4e5097ad48e07.png)

### 函数返回值

return 字样可存在也可不存在

return 只能为 return [0-255]，此处的返回可作为函数执行的状态，通过 $? 获取的就是这个返回值。

如果不加return ， 则默认最后一条语句的执行状态所为函数执行状态的返回值，如果最后一条语句执行成功，则 $? 为0，否则不为 0。

### 使用函数返回值

return 返回的数字，只是作为函数执行状态的返回值，也就是 $? 获取的值。

对于类似于下面的 `BIN=abs_path` 语句，获取的是函数体内所有的 echo、printf 输出组合成的一个字符串。

```shell
abs_path() {
    SOURCE="${BASH_SOURCE[0]}"
    while [ -h "$SOURCE" ]; do
        DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"
        SOURCE="$(readlink "$SOURCE")"
        [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
    done
    echo "test"
    echo "$(cd -P "$(dirname "$SOURCE")" && pwd)" # 此函数的两个 echo 输出会组合成一个字符串作为下述BIN的值
}

BIN=abs_path # BIN赋值函数返回值，如果没有return，则函数中所有的echo、printf输出组合成一个字符串传入BIN
path=${BIN}/nodetool # 可直接使用
```

## 输入输出重定向

一般情况下，每个 Unix/Linux 命令运行时都会打开三个文件：

1. 标准输入文件 (stdin)：stdin 的文件描述符为 0，Unix 程序默认从 stdin 读取数据。
2. 标准输出文件 (stdout)：stdout 的文件描述符为 1，Unix程序默认向 stdout 输出数据。
3. 标准错误文件 (stderr)：stderr 的文件描述符为 2，Unix程序会向 stderr 流中写入错误信息。

默认情况下，command > file 将 stdout 重定向到 file，command < file 将stdin 重定向到 file。

如果希望执行某个命令，但又不希望在屏幕上显示输出结果，那么可以将输出重定向到 /dev/null：

### 输入重定向

1. bash.sh < file ： 将脚本的输入重定向到 file，由 file 提供参数。

### 输出重定向

1. bash.sh > file ： 将脚本的输出数据重定向到 file 中，覆盖数据
2. bash.sh >> file ： 将脚本的输出数据重定向到 file 中，追加数据
3. command >> file 2>&1 ： 将 stdout 和 stderr 合并后重定向到 file

### 读取外部输入

命令：`read arg` （脚本读取外部输入并赋值到变量上）

在 shell 脚本执行到上述命令时，停止脚本执行并等待外部输入，将外部输入赋值到 arg 变量上，继续执行脚本。

## 文件引用

引用其他的文件之后，可以使用其变量、函数等等，相当于将引用的文件包含进了当前文件。

两种方式：

1. **.** file_path\file_name
2. **source** file_path\file_name

## 颜色标识

```shell
printf "\033[32m SUCCESS: yay \033[0m\n";
printf "\033[33m WARNING: hmm \033[0m\n";
printf "\033[31m ERROR: fubar \033[0m\n";
```

输出结果：

![](https://cdn.xiaobinqt.cn//xiaobinqt.io/20250430/cda90efde8424d77aec0e9aea2f3169a.png)

## 长句换行

在 shell 中为避免一个语句过长，可以使用 `\` 进行换行，使用 `\` 换行，在脚本执行过程中还是当做一行一个语句执行，不同于 enter 直接换行。

注意：`\` 前添加一个空格 。 `\` 后无空格直接换行。

```shell
/mysql/bin/mysql \
-h test_host -P 000 \
-u test_user -ptest_password ;
```

下面案例为登录mysql，并选择操作数据库，之后进行导入数据

```shell
/mysql/mysql/bin/mysql \
-h test_host -P 000 \
-u test_user -ptest_password \
-e "use test_database; source data_faile; " # -e 代表执行sql语句
```

- -u 用户名
- -p 用户密码
- -h 服务器ip地址
- -D 连接的数据库
- -N 不输出列信息
- -B 使用 tab 键 代替 分隔符
- -e 执行的SQL语句

退出脚本命令：exit

在退出脚本时使用不同的错误码，这样可以根据错误码来判断发生了什么错误。

在绝大多数 shell 脚本中，exit 0 表示执行成功，exit 1 表示发生错误。对错误与错误码进行一对一的映射，这样有助于脚本调试。

## 命令：set -e 或者 set +e

`set -e` 表示从当前位置开始，如果出现任何错误都将触发 exit。相反，`set +e` 表示不管出现任何错误继续执行脚本。

如果脚本是有状态的（每个后续步骤都依赖前一个步骤），那么请使用`set -e`，在脚本出现错误时立即退出脚本。

如果要求所有命令都要执行完（很少会这样），那么就使用`set +e`。

## 脚本调试

检查是否有语法错误 -n：

```shell
bash -n script_name.sh
```

使用下面的命令来执行并调试 Shell 脚本 -x：

```shell
bash -x script_name.sh
```

调试 count_odd_number.sh 程序案例：

```shell
# 用于计算数组中奇数的和
sum=0
for num in 1 2 3 4; do
    re=${num}%2
    if ((${re} == 1)); then
        sum=$((${sum} + ${num}))
    fi
done
echo ${sum}

```

首先检查有无语法错误：

```shell
bash -n count_odd_number.sh
```

没有输出，说明没有错误，开始实际调试：

```shell
bash -x count_odd_number.sh
```

调试结果如下：

![](https://cdn.xiaobinqt.cn//xiaobinqt.io/20250430/61b43400210c4aa7a1aee69376bc1ca4.png)

其中的输出显示了程序执行的每一步，通过观察程序执行的步骤是否满足预期从而达到调试的效果。

带有 + 表示的是 Shell 调试器的输出，不带 + 表示程序的输出。

案例：

这是 ElasticSearch 官方启动服务的脚本，看可不可以理解。

```shell
#!/usr/bin/env bash

# CONTROLLING STARTUP:
#
# This script relies on a few environment variables to determine startup
# behavior, those variables are:
#
#   ES_PATH_CONF -- Path to config directory
#   ES_JAVA_OPTS -- External Java Opts on top of the defaults set
#
# Optionally, exact memory values can be set using the `ES_JAVA_OPTS`. Note that
# the Xms and Xmx lines in the JVM options file must be commented out. Example
# values are "512m", and "10g".
#
#   ES_JAVA_OPTS="-Xms8g -Xmx8g" ./bin/elasticsearch

source "`dirname "$0"`"/elasticsearch-env

parse_jvm_options() {
  if [ -f "$1" ]; then
    echo "`grep "^-" "$1" | tr '\n' ' '`"
  fi
}

ES_JVM_OPTIONS="$ES_PATH_CONF"/jvm.options

ES_JAVA_OPTS="`parse_jvm_options "$ES_JVM_OPTIONS"` $ES_JAVA_OPTS"

# manual parsing to find out, if process should be detached
if ! echo $* | grep -E '(^-d |-d$| -d |--daemonize$|--daemonize )' > /dev/null; then
  exec \
    "$JAVA" \
    $ES_JAVA_OPTS \
    -Des.path.home="$ES_HOME" \
    -Des.path.conf="$ES_PATH_CONF" \
    -cp "$ES_CLASSPATH" \
    org.elasticsearch.bootstrap.Elasticsearch \
    "$@"
else
  exec \
    "$JAVA" \
    $ES_JAVA_OPTS \
    -Des.path.home="$ES_HOME" \
    -Des.path.conf="$ES_PATH_CONF" \
    -cp "$ES_CLASSPATH" \
    org.elasticsearch.bootstrap.Elasticsearch \
    "$@" \
    <&- &
  retval=$?
  pid=$!
  [ $retval -eq 0 ] || exit $retval
  if [ ! -z "$ES_STARTUP_SLEEP_TIME" ]; then
    sleep $ES_STARTUP_SLEEP_TIME
  fi
  if ! ps -p $pid > /dev/null ; then
    exit 1
  fi
  exit 0
fi

exit $?
```

## 参考

- [Linux-Shell脚本基础](https://misishijie.com/misc/linux-scripting-series/index.html)
- [一篇教会你写90%的shell脚本](https://zhuanlan.zhihu.com/p/264346586?share_code=lWSOCylxmY9R&utm_psn=1900283320606123913)
