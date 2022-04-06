# C语言定义字符串的方法


```c
#include <stdio.h>

int main(void) {
    char a[6] = {'F', 'i', 's', 'h', 'C', '\0'}; // 需要主动加上 \0
    char a1[] = {'F', 'i', 's', 'h', 'C', '\0'}; // 需要主动加上 \0
    char a2[] = {"FishC"};
    char a3[] = "FishC";

    printf("a: %s \n", a);
    printf("a1: %s \n", a1);
    printf("a2: %s \n", a2);
    printf("a3: %s \n", a3);

    return 0;
}
```

运行结果：

![c语言定义字符串](https://cdn.xiaobinqt.cn/xiaobinqt.io/20220314/9f05ca5175f047a2ae277ee9d99a1d55.png?imageView2/0/interlace/1/q/50|imageslim ' ')




