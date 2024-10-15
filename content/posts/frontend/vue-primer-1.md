---
title: "Vue 五小时基础入门（一）"
subtitle: ""

init_date: "2023-08-23T13:53:43+08:00"

date: 2023-08-23

lastmod: 2023-08-23

draft: true

author: "xiaobinqt"
description: "xiaobinqt,"

featuredImage: ""

featuredImagePreview: ""

reproduce: false

translate: false

tags: [ "vue" ]
categories: [ "web" ]
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

## Vue的基本使用

1. 导入vue.js

到 [vue.js](https://v2.cn.vuejs.org/v2/guide/installation.html#CDN) 网站上下载

```
<script src="../js/vue.js"></script>
```

2. 实例化Vue

创建 Vue 实例，在 html 文件里面创建一个用来接收 vue 界面的容器，用 {{ }} 来接数据

```js
<body>    <!-- 准备好一个容器 Vue构建的界面的存放位置-->
    <div id="root">
        <h1>Hello, {{name}}</h1>
    </div>
    <script>Vue.config.productionTip = false
        new Vue({el: '#root', data: {name: 'xiaobinqt'}})
    </script>
</body>
```

注意：

1. 容器和 Vue 实例是一一对应的，不能有多个相同选择器名字的容器，也不能有多个用于相同容器的 Vue 实例

2. 真实开发中只有一个 Vue 实例，并且会配合着组件一起使用

3. {{xxx}} 中的 xxx 要写 js 表达式，且 xxx 可以自动读取到 data 中的所有属性

4. 一旦 data 中的数据发生改变，那么页面中用到该数据的地方都会自动更新

### 模板语法

1. 插值语法：

功能：用于解析标签体内容

写法: {{xxx}}，xxx 是 js 表达式，且可以直接读取到 data 中的所有数据

2. 指令语法

功能：用于解析标签（包括：标签属性、标签体内容、绑定事件···）

举例：`v-bind:href='xxx'` 或简写为 `:href='xxx'`，xxx 同样要写 js 表达式，且可以直接读取到 data 中的所有数据

> Vue 中有很多的指令，且形式都是：v-???

### 数据绑定

1. 单向数据绑定

v-bind 指令，数据只能从 data 流向页面

2. 双向数据绑定

v-model 指令，数据不仅能从 data 流向页面，还可以从页面流向 data

```vue
v-bind:value="name">
v-model:value="xiaobinqt"
```

简写：

```vue
:value="name">
v-model="xiaobinqt"
```

注意：

1. 双向绑定一般都应用在表单类元素上（如：input，select）

2. v-model:value 可以简写为 v-model，因为 v-model 默认收集的就是 value 值

### el和data的两种写法

1. el的两种写法

```js
 const v = new Vue({
    // el: '#root',//第一种写法
    data: {
        name: 'xiaobinqt'
    }
})
v.$mount('#root')//第二种写法
```

2、data的两种写法

```js
new Vue({
    el: '#root',
    // 第一种写法
    // data: {
    //     name: 'xiaobinqt'
    // }

    // 第二种写法：函数式
    data() {
        return {
            name: 'xiaobinqt'
        }
    }
})
```

### MVVM模型

1、M：模型（Model）：对应 data 中的数据

2、V：视图（View）：模板

3、VM：视图模型（ViewModel）：Vue实例对象

![mvvm](https://cdn.xiaobinqt.cn/xiaobinqt.io/20230826/99738bb7efe544999707fca33289fffe.png)

总结：

1. data中所有的属性最后都出现在了vm身上

2. vm身上所有的属性 及 Vue原型上所有属性，在Vue模板中都可以直接使用

### 数据代理

1、Object.defineProperty方法

（1）

![](https://img-blog.csdnimg.cn/91422987fc03492b9cbcf94884e9acb8.png)

![](https://img-blog.csdnimg.cn/265add84bb6c4a67b843f25401e06319.png)

注意：age属性不可以枚举（遍历）

（2）

![](https://img-blog.csdnimg.cn/f989c462c642430b99a75eac197e2263.png)

![](https://img-blog.csdnimg.cn/44c2d61fdd434bc58f25510e329e6fe6.png)

注意：age属性可以被枚举，但是不能被更改

（3）

```
    <script>let person = {name: '张三',sex: '男'        }Object.defineProperty(person, 'age', {value: 18,enumerable: true, Writable: true, configurable: true,         })console.log(person)    </script>
```

（4）get和set属性的用法，将number和age联系起来，当修改number属性时，age属性的值跟着变化，反之亦然。

```
    <script>let number = 18let person = {name: '张三',sex: '男'        }Object.defineProperty(person, 'age', {get() {console.log('有人读取age属性了')return number            },set(value) {console.log('有人修改了age属性，且值是', value)                number = value            }        })console.log(person)    </script>
```

2、何为数据代理

数据代理：通过一个对象代理对另一个对象中属性的操作（读、写）

```
    <!-- 数据代理：通过一个对象代理对另一个对象中属性的操作（读、写） --> <script>let obj = {x: 100}let obj2 = {y: 200}Object.defineProperty(obj2, 'x', {get(){return obj.x            },set(value) {                obj.x = value            }        })</script>
```

3、Vue中的数据代理

![](https://img-blog.csdnimg.cn/7256fb0ef79948dbb1d2a9c2a00a33fe.png)

总结：

（1） Vue中的数据代理：通过vm对象来代理data对象中属性的操作（读/写）

（2）好处：更加方便地操作data中的数据

（3）基本原理：通过Object.defineProperty（）把data对象中所有属性添加到vm上。为每一个添加到vm的属性，都指定一个getter和setter，在getter和setter内部去操作（读/写）data中对应的数据。

## 二、事件处理

### 2.1 事件的基本使用

```
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title><script src="../js/vue.js"></script></head><body><div id="root"><h2>欢迎来到{{name}}</h2><button @click="showInfo1">点我提示信息1(不传参)</button><button @click="showInfo2($event, 66)">点我提示信息2(传参)</button></div><script>Vue.config.productionTip = falseconst vm = new Vue({el: '#root',data: {name: 'xiaobinqt'            },methods:{showInfo1(event){console.log(event)console.log(this)                },showInfo2(event, number){console.log(event, number)                }            }        })</script></body></html>
```

总结：

1、使用v-on:xxx或 @xxx绑定事件，其中xxx是事件名

2、事件的回调需要配置在methods对象中，最终会在vm上

3、methods中配置的函数，不要用箭头函数，否则this就不是vm了

4、methods中配置的函数，都是被Vue所管理的函数，this指向是vm或者组件实例对象

5、@click="demo"和@click="demo（$event）"效果一致，但后者可以传参

### 2.2 事件修饰符

1、prevent：阻止默认行为（常用）

2、stop：阻止事件冒泡（常用）

3、once：事件只触发一次（常用）

4、capture：使用事件的捕获模式

5、self：只有event.target是当前操作的元素才触发事件

6、passive：事件的默认行为立即执行，无需等待事件回调函数执行完毕

可以写多个修饰符，中间用.隔开

使用方法：

![](https://img-blog.csdnimg.cn/6e8bbdc52a4b4453aae395ea587308ab.png)

### 2.3 键盘事件

1、Vue中常用的别名

（1）回车：enter

（2）删除：delete

（3）退出：esc

（4）空格：space

（5）换行：tab（特殊，必须配合keydown使用）

（6）上：up

（7）下：down

（8）左：left

（9）右：right

2、Vue未提供别名的按键，可以使用按键原始的key值去绑定，但注意要转为kebab-case（短横线命名）

3、系统修饰键（用法特殊）：ctrl、alt、shift、meta

（1）配合keyup使用：按下修饰键的同时，再按下其他键，随后释放其他键，事件才被触发

（2）配合keydown使用：正常触发事件

4、也可以使用keyCode去指定具体的按键（不推荐）

5、Vue.config.keyCodes.自定义键名=键码，可以去定制按键别名

## 可以有多个按键触发，用.隔开

三、计算属性与监视

### 3.1 计算属性-computed

1、计算属性

```
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title><script src="./js/vue.js"></script></head><body><div id="root">        姓：<input type="text" v-model="firstName"> <br><br>        名：<input type="text" v-model="lastName"> <br><br>        全名：<span>{{fullName}}</span></div><script>Vue.config.productionTip = falseconst vm = new Vue({el: '#root',data: {firstName: '张',lastName: '三',            },computed: {fullName: {get(){return this.firstName.slice(0, 3) + '-' + this.lastName                    },set(value){const name = value.split('-')this.firstName = name[0]this.lastName = name[1]                    }                }            }        })</script></body></html>
```

注意：

（1）计算属性最终会出现在vm上，直接读取使用即可

（2）如果计算属性要被修改，那必须写set函数去响应修改，且set中要引起计算时依赖的数据发生改变

2、计算属性简写

确定计算属性只读不改才可以用简写

```
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title><script src="../js/vue.js"></script></head><body><div id="root">        姓：<input type="text" v-model="firstName"> <br><br>        名：<input type="text" v-model="lastName"> <br><br>        全名：<span>{{fullName}}</span></div><script>Vue.config.productionTip = falseconst vm = new Vue({el: '#root',data: {firstName: '张',lastName: '三',            },computed: {fullName() {return this.firstName+ '-' + this.lastName                }            }        })</script></body></html>
```

### 3.2 监视属性-watch

1、监视属性

```
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title><script src="../js/vue.js"></script></head><body><div id="root"><h2>今天天气很{{info}}</h2><button @click="changeWeather">切换天气</button></div><script>Vue.config.productionTip = falseconst vm = new Vue({el: '#root',data: {isHot: true            },computed: {info(){return this.isHot ? '炎热': '凉爽'                }            },methods: {changeWeather(){this.isHot = !this.isHot                }            },        })        vm.$watch('isHot', {mmediate: true, handler(newValue, oldValue) {console.log('isHot被修改了', newValue, oldValue);            }        })</script></body></html>
```

总结：

1、当被监视属性变化时，回调函数自动调用

2、监视的属性必须存在，才能进行监视

3、监视的两种写法：

（1）new Vue时传入watch配置

（2）通过vm.$watch监视

2、深度监视

```
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title><script src="../js/vue.js"></script></head><body><div id="root"><h2>今天天气很{{info}}</h2><button @click="changeWeather">切换天气</button><hr><h3>a的值是：{{numbers.a}}</h3><button @click="numbers.a++">点我让a+1</button><h3>b的值是：{{numbers.b}}</h3><button @click="numbers.b++">点我让b+1</button></div><script>Vue.config.productionTip = falseconst vm = new Vue({el: '#root',data: {isHot: true,numbers: {a: 1,b: 1                }            },computed: {info(){return this.isHot ? '炎热': '凉爽'                }            },methods: {changeWeather(){this.isHot = !this.isHot                }            },watch: {isHot: {immediate: true, handler(newValue, oldValue) {console.log('isHot被修改了', newValue, oldValue)                    }                },numbers: {deep: true,handler() {console.log('numbers 改变了！')                    }                }            }        })</script></body></html>
```

总结：（1）Vue中的watch默认不监视对象内部值的改变（一层）（2）配置deep：true可以检测对象内部值改变（多层）

注意：

（1）Vue自身可以检测对象内部值的改变，但Vue提供的watch默认不可以

（2）使用watch时根据数据的具体结构，决定是否采用深度监视

### 3.3 计算属性（computed）和监视属性（watch）之间的区别

1、computed能完成的功能，watch都可以完成

2、watch能完成的功能，computed不一定能完成，例如：watch可以进行异步操作

两个重要的原则：

1、所有被Vue管理的函数，最好写成普通函数，这样this的指向是vm或组件实例对象

2、所有不被Vue管理的函数（定时器的回调函数、Ajax的回调函数等），最好写成箭头函数，这样this的指向才是vm或组件实例对象

## 四、class和style绑定

### 4.1 class 绑定

![](https://img-blog.csdnimg.cn/7e33c96e877a4cd0bdffa0607ea1a625.png)

![](https://img-blog.csdnimg.cn/75568de438804f479902500fb4996be9.png)

总结：

1、写法：：class=“xxx”,xxx可以是字符串、对象、数组

2、字符串写法适用于：类名不确定，要动态获取

3、数组写法适用于：要绑定多个样式，个数不确定，名字也不确定

4、对象写法适用于：要绑定多个样式，个数确定，名字也确定，但不确定用不用

### 4.2 绑定style

![](https://img-blog.csdnimg.cn/1cf89c73c770426fad455a6f4ed51dc8.png)![](https://img-blog.csdnimg.cn/fe48f4a54fd94e818f328b4c2c61532c.png)

总结：

1、写法：：style="xxx"， xxx可以是对象，数组

2、：style="{fontSize: xxx}",其中xxx是动态值

3、:style="\[a,b\]",其中a和b是样式对象

## 五、条件渲染

### 5.1 条件渲染指令

v-show，v-if，v-else-if ，v-else

### 5.2 基本使用

![](https://img-blog.csdnimg.cn/43a0c71b1eb34a36a08fb9ac31a3bebd.png)

### 5.3 总结

1、v-if

写法：

（1）v-if="表达式"

（2）v-else-if= "表达式"

（3）v-else = "表达式"

适用于：切换频率较低的场景

特点：不展示的DOM元素直接被移除

注意：v-if可以和v-else-if 、v-else一起使用，但要求结构不能被打断

2、v-show

写法：v-show="表达式"

适用于：切换频率较高的场景

特点：不展示的DOM元素未被移除，仅仅是使用样式隐藏掉

3、注意：使用v-if时，元素可能无法被获取到，而使用v-show一定可以获取到

## 六、列表渲染

### 6.1 基本使用

```
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>基本列表</title><script src="../js/vue.js"></script></head><body><div id="root"><h2>人员列表(遍历数组)</h2><ul><li v-for="(p, index) in persons" ::key="index">{{p.name}}-{{p.age}}</li></ul><h2>汽车信息(遍历对象)</h2><ul><li v-for="(value, key) in car" ::key="key">{{key}}-{{value}}</li></ul><h2>测试遍历字符串</h2><ul><li v-for="(char, index) in str" ::key="index">{{char}}-{{index}}</li></ul><h2>测试遍历指定次数</h2><ul><li v-for="(number, index) in 5" ::key="index">{{number}}-{{index}}</li></ul></div><script>Vue.config.productionTip = falsenew Vue({el: '#root',data: {persons: [                {id: '001', name: '张三', age: 18},                {id: '002', name: '李四', age: 19},                {id: '003', name: '王五', age: 20}                ],car: {name: '奥迪A8',price: '70万',color: '黑色'                },str: 'hello'            }        })</script></body></html>
```

### 6.2 key的原理

![](https://img-blog.csdnimg.cn/4b0a9aa4286c4d4da784be7bc9048c96.png)

![](https://img-blog.csdnimg.cn/056030631d4b4e91bfaf14372320c024.png)

如果没有写key，key默认是index

### 6.3 总结

1、虚拟DOM中key的作用 ：key是虚拟DOM对象的标识，当数据发生变化时，Vue会根据【新数据】生成【新的虚拟DOM】，随后Vue进行【新虚拟DOM】与【旧虚拟DOM】的差异比较，比较规则如下：

2、对比规则：

（1）旧虚拟DOM中找到了与新虚拟DOM相同的key：

① 若虚拟DOM中内容不变，直接使用之前的真实DOM

②若虚拟DOM中内容变了，则生成新的真实DOM，随后替换掉页面中之前的真实DOM

（2）旧虚拟DOM中没有找到与新虚拟DOM相同的key

创建新的真实DOM，随后渲染到页面

3、用index作为key可能引发的问题：

（1）若对数据进行：逆序添加、逆序删除等破坏顺序操作：会产生没有必要的真实DOM更新=>界面效果没问题，但效率低

（2）如果结构中还包含了输入类的DOM：会产生错误DOM更新==>界面有问题

4、开发中如何选择key：

（1）最好使用每条数据的唯一标识作为key，比如id、手机号、身份证号、学号等唯一值

（2）如果不存在对数据的逆序添加、逆序删除等破坏顺序操作，仅用于渲染列表用于展示，使用index作为key是没有问题的

## 七、Vue监测数据的原理

1、Vue会监视data中所有的数据

2、如何监测对象中的数据：

通过setter实现监视，且要在new Vue时就传入要监测的数据

（1）对象中后追加的属性，Vue默认不做响应式处理

（2）如需给后添加的属性做响应式，请使用如下API：

Vue.set(target, propertyName/index, value)或者vm.$set(target, propertyName/index, value)

3、如何监测数组中的数据：

通过包裹数组更新元素的方法实现，本质就是做了两件事：

（1）调用原生对应的方法对数组进行更新

（2）重新解析模板，进而更新页面

4、在Vue修改数组中的某一个元素一定要用如下方法:

（1）使用这些API：push（)、pop（）、shift（）、unshift（）、splice（）、sort（）、reserve（）

（2）Vue.set（）和vm.$set（）

5、特别注意：Vue.set（）和vm.$set（）不能给vm或者vm的根数据对象添加属性

## 八、收集表单数据

1、若：<input type="text"/>,则v-model收集的是value值，用户输入的就是value值。

2、若：<input type="radio"/>，则v-model收集的是value值，且要给标签配置value值。

3、若：<input type="checkbox"/>：

（1）没有配置input的value属性，那么收集的就是checked（勾选or未勾选，是布尔值）

（2）配置input的value属性：

①v-model地初始值是非数组，那么收集地就是checked（勾选or未勾选，是布尔值）

②v-model的初始值是数组，那么收集的就是value组成的数组

4、备注：

v-model的三个修饰符：

（1）lazy：失去焦点再收集数据

（2）number：输入字符串转为有效的数字

（3）trim：输入首位空格过滤

## 九、过滤器

1、定义： 对要显示的数据进行特定格式化后再显示（适用于一些简单逻辑的处理）

2、语法：

（1）注册过滤器： Vue.filter(name, callback)或 new Vue（filters： { }）

（2）使用过滤器： {{ xxx | 过滤器名}}或 v-bind:属性 = “xxx | 过滤器名”

3、备注：

（1）过滤器也可以接收额外参数、多个过滤器也可以串联

（2）并没有改变原来的数据，是产生新的对应的数据

## 十、内置指令

### 10.1 v-text指令

1、作用：向其所在的节点中渲染文本内容（将所有内容都当做文本内容，不会解析标签）

2、与插值语法的区别：v-text会替换掉节点中的内容，{{xxx}}则不会

### 10.2 v-html 指令

1、作用：向指定节点中渲染包含html结构的内容

2、与插值语法的区别：

（1）v-html会替换掉节点中所有的内容，{{xxx}}则不会

（2）v-html可以识别html结构

3、严重注意：v-html有安全性问题

（1）在网站上动态渲染任意HTML是非常危险的，容易导致XSS攻击

（2）一定要在可信的内容上使用v-html，永远不要用在用户提交的内容上

### 10.3 v-cloak 指令

1、本质是一个特殊属性，Vue实例创建完毕并接管容器后，会删掉v-cloak属性

2、使用css配合v-cloak可以解决网速慢时页面展示出{{xxx}}的问题

### 10.4 v-once 指令

![](https://img-blog.csdnimg.cn/3403fa61e5874efdb20508e9dca3aa22.png)

1、v-once所在节点在初次动态渲染后，就视为静态内容了

2、以后数据的改变不会引起v-once所在结构的更新，可以用于优化性能

### 10.5 v-pre指令

1、跳过其所在节点的编译过程

2、可利用它跳过：没有使用指令语法。没有使用插值语法的节点，会加快编译

## 十一、自定义指令

```
<script>Vue.config.productionTip = falseVue.directive('fbind', {bind(element, binding){            element.value = binding.value        },inserted(element, binding){            element.focus()        },update(element, binding){            element.value = binding.value        }    })new Vue({el: '#root',data: {n: 1        },        directives :{big(element, binding) {                element.innerText = binding.value * 10            },        }    })</script>
```

### 11.1 定义语法

1、局部指令：

new Vue（{

directives：{指令名：配置对象}

}）

或者

new Vue（{

directives ：{指令名（）{函数体内部}}

}）

2、全局指令

Vue.directive（指令名，配置对象）或者Vue.directive（指令名，回调函数）

### 11.2 配置对象中常用的3个回调函数

1、bind：指令与元素成功绑定时调用

2、inserted：指令所在元素被插入页面时调用

3、update：指令所在模板结构被重新解析时调用

### 11.3 注意事项

1、指令定义时不加v-，但使用时要加上

2、指令名如果是多个单词，要使用kebab-case命名方式，不要用camelCase命名，在定义时，要将指令名用单引号''包起来

## 十二、生命周期

```
<script>Vue.config.productionTip = falsenew Vue({el: '#root',data: {opacity: 1        },methods: {        },mounted(){setInterval(() => {this.opacity -= 0.01if(this.opacity <= 0) this.opacity = 1            }, 16)        }    })</script>
```

1、生命周期又名生命周期回调函数、生命周期函数、生命周期钩子

2、生命周期是Vue在关键时刻帮我们调用的一些特殊名称的函数

3、生命周期函数的名字不可修改，但函数的具体内容是程序员根据需求编写的

4、生命周期函数中的this指向是vm或 组件实例对象

![](https://img-blog.csdnimg.cn/cf291b2f27f84eaa89641db4be80d92e.png)

![](https://img-blog.csdnimg.cn/bfe2dcb46f434cfebc61b89d9edb708a.png)

5、常用的生命周期钩子：

（1）mounted：发送Ajax请求、启动定时器、绑定自定义事件、订阅消息【初始化操作】

（2）beforeDestroy：清除定时器、解绑自定义事件、取消订阅消息等【收尾工作】

6、关于销毁Vue实例

（1）销毁后借助Vue开发者工具看不到任何信息

（2）销毁后自定义事件会失效，但原生DOM事件仍然有效

（3）一般不会在beforeDestroy操作数据， 因为即使操作数据，也不会再触发更新流程了

## 参考

+ [Vue](https://blog.csdn.net/weixin_58598560?type=blog)





