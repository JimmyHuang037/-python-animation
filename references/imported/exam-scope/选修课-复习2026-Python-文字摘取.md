# 选修课复习2026：逐页文字摘取

来源：选修课-复习2026-Python.pptx。只用于内容范围核对；图片中的代码未全部转录，不能替代原件。

## 第1页

0 编程语言与编程环境

图片对象数：1

## 第2页

选择题    30分（15*2）模块 标识符 数据类型与运算符 输入输出 分支结构 循环结构 列表 字符串 字典 绘图 词云 函数 正则 爬虫 文件读写
填空题    20分（3*2+3*2+4*2）
                   图形打印、字典统计+写文件TXT、函数+tkinter(label、button、entry、text)
简答题    20分（4*5）
                  程序结构 数据类型 正则与爬虫 词频分析与词云
编程题    30分（3*10）
                  程序结构  matplotlib绘图  基于文件CSV的统计分析
考试题型：
考试形式：闭卷机考（教务处通知）信息楼机房

图片对象数：1

## 第3页

Python有强大的标准库和丰富的第三方库        
标  准  库：https://docs.python.org/3.8/library/
            如：math、 random 、webbrowser、calendar、tkinter、re等
第三方库： https://pypi.org/
            如：matplotlib、wordcolud 、numpy、requests等，需要安装
Python库简介

图片对象数：1

## 第4页

第三方库安装
可以安装的模块可以在https://pypi.org/中查找
运行->cmd进入命令提示符
pip install 库名，例如： pip install matplotlib
第三方模块必须先安装，才能导入

图片对象数：2

## 第5页

import语句，语法格式：import <模块名> 
import math			#导入math库
num= 3000
result=math.sqrt(num)	#计算平方根
print('结果是：',result)	#打印
库/模块的导入
 也可以在一行内导入多个模块：
    import <模块1> [,<模块2> [, …<模块n>]] 
import time, math, calendar
导入方式不一样，模块中的库函数引用的方式就不一样.

图片对象数：1

## 第6页

用as来给它取别名
import math as mt			#导入math库
import matplotlib.pyplot as plt       #取别名
tmax=mt.sqrt(200)		

图片对象数：1

## 第7页

使用库/模块中的某些函数、某些变量、某些类
语法格式： from 模块名 import  函数名
from math import sqrt	#导入math模块中的sqrt()函数
t= sqrt(9) 				#调用sqrt()函数
语法格式： from 模块名 import  *
from math import *		#导入math模块中的所有名称
t= sqrt(9) 				#调用sqrt()函数
注意： 如果导入多个库时可能会造成同名函数的覆盖，故慎用！

图片对象数：1

## 第8页

1   基本语法、三大结构、函数

图片对象数：1

## 第9页

程序
算法
数据
常量
变量
基本运算
程序结构
数据类型
基本运算符
三种程序结构
转义字符
值常量(数字，字符串，False)
不改变值的变量（其他语言：命名常量或者符号常量）

图片对象数：0

## 第10页

合法的标识符必须遵守以下规则：
由一串字符组成，字符可以是任意字母、数字、下画线、汉字，但这串字符中的开头字符不能是数字；
不能与关键字同名。关键字也称为“保留字”，是被语言保留起来具有特殊含义的词，不能再用于起名字。
标识符（名称）
例：m.n	math-score	     3AI	for    break 

图片对象数：0

## 第11页

Python的数据类型
strS='this is string'
var1=False
num2=2.3
nums=[1, 3, 5, 7, 8, 13, 20]
tup1 = (1, 2, 3, 4, 5 )
dict1 = {'name': 'Zara', 'age': 7, 'class': 'First'}
num1=5

图片对象数：1

## 第12页

布尔值（逻辑值）
布尔值：True(1)、False(0)，可进行算术运算。
注意：
x=5
if  x:
    print("x是%d" % x)

图片对象数：1

## 第13页

算术运算符的优先级，按照从低到高排列
算术运算符

图片对象数：2

## 第14页

赋值运算
例：
例：
变量
赋值符
S2 = pi*(2.2/2)**2
变量 = 表达式
序列赋值
a,b=2,8     或 no1,no2,no3,no4,no5="hello"
多目标赋值
no1=no2=no3=no4=no5="hello"
复合赋值。形式：算术运算符＝
a+=3  等价于　a=a+3
那么a*＝b+1  等价于? 

图片对象数：0

## 第15页


图片对象数：1

## 第16页

关系运算符
>	：x>0
<	：x<0
>=	：x>=0
<=	： 'a'<= 'A'                  # 比较ASCII码值
==	：等于，如x==0
!=	：不等于，如x!=0
关系运算符也称为比较运算符，可以对两个数值型或字符串型数据进行大小比较，返回一个“True”或“False”的布尔值

图片对象数：0

## 第17页


图片对象数：1

## 第18页

逻辑运算符
and：与（而且）
例：“x>=-1 and x<=1“  
注：也可写成   -1<=x<=1 
or：或（或者）
例：x>1 or x<-1     
not：非（不是）
例：not 3>8

图片对象数：0

## 第19页

input()函数
格式：变量名 = input(<提示字符串>)
作用：从键盘读入一个字符串
age=int(input('请输入你的年龄：'))
print('你的出生年份为：', 2023-age)
name=input('请输入你的姓名：')
print('你的名字叫：', name)
int()函数
float()函数

图片对象数：0

## 第20页

print()函数
格式：print(<输出值1>,<输出值2>, … , sep=' ', end='\n')
作用：打印输出括号中的内容
print('Hello World!')
字符串用单/双引号括起来
print("Hello","World")
print("abc"*3)
name="张三"
age=20
print("Hello",name,age)
print("Hello",end='')
print("Hello")
print("Hello",end='')

图片对象数：0

## 第21页

字符串的格式化
用%格式字符的一般形式是：format_string % obj
作用：把对象obj按格式要求转换为字符串:
print ("%s的年龄是%d" % ("张三",20))
print ("我的名字是%s" % "张三")
name="张三"
print ("我的名字是%s" % name)
name="张三"
score=86.345
print ("%s的成绩是%.1f" % (name, score))

图片对象数：0

## 第22页

常见格式字符见表

图片对象数：1

## 第23页

格式化辅助指令

图片对象数：1

## 第24页

 顺序结构：自上而下依次执行各条语句；
 选择/分支结构：分支结构指程序根据不同的条件执行不同的分支语句；if语句，if-else语句，if-elif-else语句
 循环结构：循环结构指程序根据特定的条件重复执行语句；while循环，for循环
程序设计的三种结构

图片对象数：0

## 第25页

if-else分支结构
if   条件表达式1:
      语句组一
elif 条件表达式2: 
      语句组二
else:
      语句组三
例：  score=float(input("请输入成绩："))
         if score>=85:
             print("%.1f分，成绩优" % score)
         elif score>=60:
             print("%.1f分，已及格" % score)
         else:
             print("%.1f分，不及格" % score)
条件表达式可以是任意类型，如5>3，x==y，x and y>z，3，0等。其中，非0（如： 3 ）表示恒真（即True），而0表示恒假（即False）

图片对象数：1

## 第26页

例：数值成绩等级转换。
x=float(input("请输入成绩："))
if  x>=85:
    print("%f分，成绩优" % x)
elif  x>=70:
    print(" %f分，成绩良" % x)
elif  x>=60:
     print("%f分，已及格" % x)
else:
     print("%f分，不及格" % x)
　　　 优         (85=<x<100)
等级=  良         (70=<x<85)
            及格      (60=<x<70)
            不及格   (x<60)

图片对象数：0

## 第27页

while循环
例：
time=8
while time<12:
    print("Doing homework",end=',')
    time=time+1
    while 条件表达式： 
           语句组

图片对象数：1

## 第28页

for循环
将L中的元素依次取出赋给x，每取一个元素，执行一次循环体
for x in L:
    语句1
    ……
    语句n
循环体

图片对象数：1

## 第29页

for循环
for 循环变量 in 对象:
      语句块A
else:                           #可选
      语句块B
例：
k=0
for i in range(100,201): 
    if i%7==0:
        k+=1
print(k)
字符串、列表、元组、字典、
迭代器

图片对象数：0

## 第30页

range()函数
功能：用于生成整数等差数列
格式： range(start, end, step)
例：
     程序运行结果为：4 6 8
for iNum in range(4,10,2):
    print(iNum,end=" ") # 注意end的用法
range(1,100,2)
range(100,1,-2)
range(100)

图片对象数：0

## 第31页

循环控制语句
 break
    中断循环的执行，跳出循环体
continue
    中断本次循环，进入下一次循环判断
例：
sentence=input("请输入一段文字：")
for word in sentence:             #这是个秘密秘密秘密！
    if word=="密":
        break/continue
    print(word,end="")            #这是个秘秘秘！

图片对象数：0

## 第32页

思考题
如何使用循环输出如下所示的菱形图形？

图片对象数：1

## 第33页

思考题答案
fh=input("请输入一个字符：")
blank=' '
n = int(input("请输入上三角行数："))
for i in range(n):
    print(blank*(n-i-1),end='')
    print(fh*(2*i+1))
for i in range(n-1):
    print(blank*(i+1),end='')
    print(fh*(2*(n-i-1)-1))

图片对象数：0

## 第34页

8、试输出如下图形，要求输入行数：
 
line=int(input("请输入行数:"))
while line%2==0:
    line=int(input("请输入奇数:"))    
n=(line+1)//2
blank=' '
for i in range(n):
    print(blank*(n-i-1),end='')
    print(chr(65+i)*(2*i+1))
for i in range(n-1):
    print(blank*(i+1),end='')
    print(chr(65+n-i-2)*(2*(n-i-1)-1))

图片对象数：1

## 第35页

函数是一段具有特定功能的、可重用的语句组
使用函数目的：降低编程难度和代码重用
函数分为：内置函数和用户自定义函数
函数

图片对象数：1

## 第36页

def <函数名>  (<[形参列表]>):
    <执行语句>
    [return <返回值>]
函数定义
例如：
def myfunc(x,y):
    z=x+y
    return z
myfunc(2,3)

图片对象数：1

## 第37页

<函数名>  ([实参列表])
在语句中直接使用函数名，并在函数名之后的圆括号中写传入实际参数，多个参数之间以半角逗号隔开。例如：myfunc(2,3)
注意：调用时，即使不需要传入实际参数，也要带空括号。
函数的调用

图片对象数：1

## 第38页

位置传递  参数按照定义的位置及顺序进行传递
关键字传递  通过传递的参数的名称进行识别
默认值参数传递  给某些参数设置一个默认值，如果不传则读取默认值
参数的传递

图片对象数：1

## 第39页

位置传递      实参个数=形参个数，否则报错。
 							
参数的传递
TypeError: fun1() missing 1 required positional argument: 'c'

图片对象数：2

## 第40页

关键字传递
        调用函数时，明确指定把某个实参值传递给某个形参，位置无关。
【例3】参数的关键字传递。比较两个数的大小，输出大者。
 							运行结果为：
								7
参数的传递

图片对象数：2

## 第41页

默认值参数传递      在定义函数时直接对形参赋值。
【例5】默认值参数传递。比较两个数的大小，输出大者。
 							运行结果为：
								7
参数的传递

图片对象数：2

## 第42页

定义：指变量能被有效使用的范围。
全局变量  在函数之外定义的变量，在整个程序范围内起作用。
局部变量  指在某个函数内部定义的变量，在该函数范围内起作用。
变量的作用域

图片对象数：1

## 第43页

说明：全局变量与局部变量同名
函数内部局部变量起作用，函数外部全局变量起作用。
变量的作用域
【例9】变量的作用域（一）。
运行结果为：
函数内：a=10,b=15
函数外：a=5,b=6

图片对象数：2

## 第44页

说明：全局变量与局部变量同名
函数内部局部变量起作用，函数外部全局变量起作用。
若需在函数内部修改全局变量，使用global声明。
变量的作用域
【例10】变量的作用域（二）。
运行结果为：
函数内：a=10,b=15
函数外：a=10,b=6

图片对象数：2

## 第45页

就是没有名字的函数，通常用在那些只使用一次的场景中。     lambda 参数列表 : 表达式
只能有一个表达式，表达式就是函数的返回值。
匿名函数
例：lambda x,y:x+y      函数的返回值： x+y

图片对象数：1

## 第46页

递归（recursion）是一种直接或者间接调用函数自身的算法，其实质是把问题分解成规模缩小的同类子问题，然后递归调用求出问题的解。
能够设计成递归算法的问题必须满足两个条件：
能找到反复执行的过程（调用自身）
能找到跳出反复执行过程的条件（递归出口）
函数的递归调用

图片对象数：1

## 第47页

def fac(n):
    if n==1:
        return 1
    else:
        return n*fac(n-1)
　　　 1             (n=1)   /*结束条件，基本解*/
 n! =
         　n*(n-1)! (n>=2)  /*递推公式*/
用递归算法计算正整数n的阶乘
def fac(n):
    f=1
    for i in range(1,n+1):
        f*=i
    return f
#递归函数
#普通函数

图片对象数：1

## 第48页

组合数据类型

图片对象数：1

## 第49页

字符串：属于不可变序列类型，使用单引号、双引号、三单引号或三双引号作为界定符。a = 'Python'
列表：可存储由多个值组成的序列。有序的，动态的。[]
元组：可存储由多个值组成的序列。不可改变的。()
字典：包含了一个索引的集合，称为键（key）和值（value）的集合。字典就是用花括号包裹的键值对的集合。每个键值对用冒号“:”分隔，每对之间用逗号“,”分隔
几个组合数据类型
d={'name':'alice','age':19,'sex':'F'}

图片对象数：1

## 第50页

1.字符串
包含在引号之间的字符集合，每个字符都会有一个位置标识，称为索引。
例：name=‘abcdef’
字符串
a       b      c      d      e        f
正索引
0       1       2     3      4        5 
负索引
-6     -5     -4    -3    -2      -1
Python中下标从0开始
利用方括号运算符[ ]可以通过索引值得到相应位置（下标）的字符：
①从前往后的正向索引，n个字符的字符串，其索引值从0至n-1；
②从后向前的负数索引，n个字符的字符串，其索引值从-1至-n
注意：下标不能越界

图片对象数：1

## 第51页

字符串切片a[i:j:k]
在Python程序中，可使用切片从字符串中提取子串。
切片的参数是用两个冒号分隔的三个数字：
第一个数字表示切片开始位置（默认为0）
第二个数字表示切片截止位置（但不包含这个位置，默认为字符串长度）
第三个数字表示切片的步长（默认为1），当步长省略时，可以顺便省略最后一个冒号
字符串长度  len()函数；

图片对象数：0

## 第52页

>>> a = 'Python'
>>> a[1:4]  # 切片实际包含索引位置为1～3的字符
'yth'
>>> a[:4]  # 省略第一个数字，表示切片从位置0开始
'Pyth'
>>> a[1:]  # 省略第二个数字，表示切片至字符串末尾结束
'ython'
>>> a[-2:] # 后两个字符
'on'
>>> a[::2]  # 步长为2
'Pto'
>>> a[::-1]  # 步长为-1，得到逆序字符串
'nohtyP'
>>> a[:100]  # 截止位置越界，切片到末尾结束
'Python'
>>> a[100:]  # 起始位置越界，返回空字符串	
''

图片对象数：0

## 第53页

字符串的常规操作
假设变量a =“Hello”, b =“Python”
运算符
描述
实例
结果
+
字符串连接
注意：只能将字符串与字符串拼接
a + b
HelloPython
*
重复输出字符串
a * 2
HelloHello
[]
通过索引获取字符串中字符
a[1]
e
[:]
截取字符串中的一部分，即“切片”
a[1:4]
ell

图片对象数：0

## 第54页

常用字符串方法
isdigit()：字符串非空且只有数字
isalpha()：字符串非空且只有字母
strip()：消除字符串两端空格及符号
replace()：用第二个子串替代第一个
split()：将字符串分成多个短字符串，返回列表。
upper()：将字符串都转换成大写字母 
lower()：将字符串都转换成小写字母
count():  统计字串的个数
sr = ",123Hi,every,one,321,"
>>> sr.isdigit()
>>> sr.isalpha()
>>> sr =sr.strip(",")
>>> st =sr.replace("e","a")
>>> s1,s2 =sr.split(",")

图片对象数：1

## 第55页

2.列表（List）
能保存任意数量任何数据类型的Python 对象。
列表元素用中括号[ ]包裹，元素用逗号分隔
列表是有序的、是动态的,
元素是按序编号索引的（从0开始）
元素的个数及元素的值可以改变
利用编号可对元素进行增删改查等操作（动态的）。
切片运算符[ i : j]得到从下标i到下标j-1的子集

图片对象数：0

## 第56页

添加/删除元素
添加元素
删除元素
L.insert(i, x)
L.append(x)
L.pop()
L.pop(i) 
L = ['m', 'i', 'l', 'e']
L.insert(0, 's’)                  #L=['s', 'm', 'i', 'l', 'e']
L.append('s’)              #L=['s', 'm', 'i', 'l', 'e', 's']
L =['s', 'm', 'i', 'l', 'e', ‘s’]
L.remove('m’)              #L=['s', 'i', 'l', 'e', 's'] 
L.pop(0)                     # 's’ L= ['i', 'l', 'e', 's']
L.pop()                       #’s’ L=['i', 'l', 'e']               
L.remove(x)

图片对象数：0

## 第57页

3.字典
是Python 中的映射数据类型
每个元素(item)由键-值(key-value)对构成
     d = {key1 : value1, key2 : value2 }
字典元素用大括号{ }包裹
字典是无序的
注意：键必须是唯一的，必须是不可变数据类型的，例如：字符串、    数字或元组。
            值可以是任何数据类型。
下面的字典定义为什么错误？
dict = {(1,2):['a','b'],[5,6]:['c','d'],4:('c','d'),'choice':123}

图片对象数：1

## 第58页

字典示例
>>> aDict = {'host': 'earth'}
>>> aDict['port']=80
>>> aDict
>>> aDict.keys( )    #以列表形式给出
>>> aDict.values( )
>>> aDict['host']   #输出对应的值
键
值

图片对象数：1

## 第59页

字典的方法
以键查值：dict.get(key,default=None)
例如：>>> d = {}
          >>> print (d.get('name'))        #None
          >>> d["name"] = 'Eric’
          >>> d.get('name')                   #'Eric’
          >>> d.get('age',0)                   #0
更新：dict.update(adict)
>>> d={'name':'alice','age':19,'sex':'F'}
>>> x={'name':'bob','phone':'12345678'}
>>> d.update(x)
>>> d
{'age': 19, 'phone': '12345678', 'sex': 'F', 'name': 'bob'}
删除：del dict[key] #删除键键值对

图片对象数：0

## 第60页

返回字典所有的键、值和项
dict.keys()：返回包含原字典中每项的键的列表；
dict.values()：返回包含原字典中每项的值的列表；
dict.items()：返回包含原字典中每项的项(键,值)的列表。
>>> d={'name':'alice','age':19,'sex':'F'}
>>> d.keys()
dict_keys(['age', 'sex', 'name'])
>>> d.values()
dict_values([19, 'F', 'alice’])
>>> d.items()
dict_items([('age', 19), ('sex', 'F'), ('name', 'alice')])

图片对象数：1

## 第61页

遍历所有的键-值对——字典.items( )
persons={'name':'alice','age':19,'sex':'F'}
for key,value in persons.items( ):
      print("\nKey:"+key)
      print("Value:",value)
名字可以随意起

图片对象数：1

## 第62页

3 文件、数据分析与可视化

图片对象数：1

## 第63页

文件打开方式一(打开指定位置的文件)：
    handle = open("D:\\exam\\test.txt", 'r',encoding='utf-8')  
    handle = open("D:/exam/test.csv", 'r') 
文件打开方式二(打开当前目录下文件) ：
    handle = open("test.txt", 'r',encoding='utf-8')  
文件关闭：
    handle.close( )
with open(‘test.txt’, ‘a’) as f: 语句的用法
文件打开与关闭

图片对象数：1

## 第64页

模式
说明
"r"
以只读方式打开文件（默认值）
"w"
以写方式打开(若已存在则覆盖原文件，否则新建文件)
"a"
以写方式打开，写入内容追加在文件末尾
“r+”、“w+”、"a+"
以修改方式打开，支持读取和写入
"b"
表示二进制文件，添加在其它控制字符后面
"t"
表示文本文件，默认值
文件打开模式

图片对象数：1

## 第65页

文件的读写
handle.read()：读取整个文件内容到字符串中
handle.readlines()：读取整个文件内容并存入列表
handle.readline()：读取一行内容到字符串中
  handle.write() ：一个字符串写入到文件中
  handle.writelines()：字符串或字符串列表按行写入文件中   

图片对象数：1

## 第66页

  handle.write(string) ：将字符串string的内容写到文件中，并返回写入的字符数。但不会自动换行，如果需要换行，则要使用换行符'\n’。  
string="This is Miss Zhang\n"
handle.write(string)
文件写入方式（一）
注意：文件可通过'r+' 、'w'或'a'等方式打开

图片对象数：1

## 第67页

  handle.writelines(sequence)：字符串或字符列表写入文件中   
  
string="This is Miss Zhang\n"
handle. writelines(string)
 words=["hello\n","world\n"]
 handle.writelines(words)
文件写入方式（二）

图片对象数：1

## 第68页

文本文件数据分析-由成绩，统计学科等级水平
分析：某中学对学生的附加科目进行能力测试，并按以下标准统计学科等级水平。
（1）总分达到260分为优秀；
（2）总分达到180分为及格；
（3）总分不到180分为不及格。
编程要求：从score.txt文件中读取学生成绩数据，判定等级并写入level.txt文件中，并统计每个等级的人数，结果输出到屏幕。

图片对象数：2

## 第69页

（1）读取文件score.txt数据到列表L中(如果数据存储在csv文件中的情况，自行练习)
列表L中的数据项对应着文件中的每条学生记录，通过循环语句遍历L，提取需要的考号和三门课的成绩，并存放在列表x中。
（2）判定学科等级，统计每个等级人数。
列表x包含4个数据项，x[0]为考号，x[1]、x[2]和x[3]分别为“程序设计”、“生物”和“科学”三门课的成绩，需要转换为整数类型以便进行求和等数值运算。最后通过分支语句，将求得的等级结果存放在key变量中。相应等级的人数加1。
（3）将考号和等级结果按一定格式写入文件level.txt中。在屏幕输出等级人数。
方案：

图片对象数：1

## 第70页

handle = open("score.txt", 'r')
f=open('level.txt','w')
aList=handle.readlines()
for line in aList[1:]:
    x=line.split()
    score=float(x[1])+float(x[2])+float(x[3])
    if score>=260:
        key='优秀'
elif score>=180:
        key='及格'
else:
        key='不及格'
f.write('%s\t%s\n'%(x[0],key))
f.close( )

图片对象数：2

## 第71页

词频统计问题的IPO描述
文中最常出现的若干个单词及出现的次数
处理
输出
输入
从文件中读取一篇待分析的文章
采用字典数据结构统计词语出现的频率

图片对象数：1

## 第72页

文本词频统计方法
        对于一段英文文本，希望提取其中的单词，可以使用字符串处理的split( )方法即可。
例：>>> "I am Chinese".split( )
        ['I', 'am', 'Chinese']
        对于中文“我是中国人”，获得单词非常困难。
        jieba是Python中一个重要的第三方中文分词函数库。

图片对象数：1

## 第73页

英文文本词频统计方法
第一步：找寻英文文本文件，保存为   *.txt；
第二步：使用handle.read()：读取整个文件内容到字符串中，分解并提取英文文章的单词：
通过txt.lower( )函数统一字母为小写
使用txt.replace( )方法将英文单词的分隔符（空格、标点符号或者特殊符号）统一为空格，再提取单词。
使用txt.split()方法将英文文本分割为单词列表

图片对象数：1

## 第74页

	第三步：利用字典对每个单词进行计数：设单词保存在变量word中，使用一个字典类型counts={<单词>：<出现次数> }，
无论词是否在字典中，加入字典counts中的处理逻辑可以统一表示为：
        counts[word]=counts.get(word,0)+1
得到所有单词的词频字典。
         第五步：对单词的统计值从高到低进行排序，输出前若干个高频词语，并格式化打印输出。
词频字典的使用
       第四步： 分析结果高频词汇中的冠词、代词、连接词等语法型词汇，并不能代表文章的含义。
        可以采用构建一个排除词汇库excludes，将语法型词汇排除。

图片对象数：1

## 第75页

中文文本词频统计方法-jieba库
       英文词汇之间有天然的空格分隔，而中文文章中字词之间没有分隔符号，且字词长短不一，不同的组合语义差别很大。要进行中文词频分析，首先要解决中文词汇的分割问题。
      Python的第三方库jieba是一个用于中文词汇分割的函数库，运用jieba.lcut()方法可高效准确地将字符串中的中文词汇实现分割，精确返回词汇列表。

图片对象数：1

## 第76页

wordcloud和词频可视化
词云可视化： Python的第三方库wordcloud是一种能将词语渲染成大小、颜色不一的可视化呈现形式“词云”的函数库。其效果能将枯燥呆板的文字以直观的艺术效果展示出来。

图片对象数：1

## 第77页

词云

图片对象数：3

## 第78页

词云相关库
matplotlib：用于绘图的第三方库
wordcloud：用于词云展示的第三方库
imageio： 读取和写入各种图像的第三方库

图片对象数：1

## 第79页

使用wordcloud库生成词云
1、IDLE中wordcloud库的安装
        打开cmd窗口通过pip指令安装：pip install wordcloud
 2、调用函数：w=wordcloud.WordCloud()
WordCloud()函数生成了一个WordCloud对象，之后我们对词云的一系列操作都是建立在这个对象的基础上的。
 3、另外三个函数：
      w.generate_from_frequencies(dic)  #用于根据给定的词频字典生成词云图
      w.generate (str)  #用于根据给定的文本字符串生成词云图
      w.to_file(filename)    #将生成的词云文件输入到一个文件中，完成词云文件的保存

图片对象数：1

## 第80页

WordCloud()函数的参数
font_path：字体路径	string，如font_path='msyh.ttc’
mask：绘制的词云形状，如果 mask 非空，设置的宽高值将被忽略。
width ：画布宽度int，default=400
height	：画布高度int，default=200
background_color ：背景颜色，default="black“
（如果背景要设置为透明，则需background_color=None 和 mode='RGBA'）
max_words：词的最大个数int ，default=200
scale：按照比例进行放大画布float，default=1，若1.5则长和宽都是原来画布的1.5倍
min_font_size：显示最小字体大小，default=4
max_font_size：显示最大字体大小，int/None,default=None

图片对象数：1

## 第81页

学生考勤词云
import matplotlib. pyplot as plt
from wordcloud import WordCloud
from imageio import imread
pic = imread('love.png')
counts={"李鼎文":20,"何润喆":5,"林诗怡":10,"田书翰":18,"袁立豪":15,\
        "周涛":12,"成飞飞":16,"赵楼":22,"鲁云":	12,"吴少峰":2,\
        "李文":6,"何喆":11,"林怡":9,"田书":8,"袁豪":15}
#创建一个字典

图片对象数：2

## 第82页

wc=WordCloud(mask=pic, 
            font_path='msyh.ttc',                 #中文字体为微软雅黑
             background_color='white',       #设置背景颜色
             max_words=15,                         #设置最大词数
             max_font_size=1000,     
             min_font_size=10,
             scale=1)                                     #按照比例进行放大画布
wc.generate_from_frequencies(counts)
wc.to_file('resulte.png')
plt.imshow(wc)                              #对图像进行处理,但不能显示
plt.show()

图片对象数：0

## 第83页

Matplotlib官网
库导入：import matplotlib.pyplot as plt 

图片对象数：2

## 第84页

Matplotlib常用函数
函数名称
函数作用
  figure()
  创建一个新的图形对象
   plot()
   绘图折线图
   show()
   在本机显示图形
   bar()
   绘制垂直条形/柱形图
   pie()
   绘制饼图
   scatter()
   绘制散点图
   hist()
   绘制直方图
   subplot() 
   绘制子图

图片对象数：1

## 第85页

plt.plot(x, y, s):
       x：x坐标
       y：y坐标
       s：指定线条颜色（'r'、 ‘y'、 'g' 、' b'等）、线条样式（'-' 、'--'等）和数据点形状（ ' o '、 ' s '等 ）的字符串
Matplotlib折线图函数

图片对象数：1

## 第86页

功能强大的科学计算库, 提供大量的数学函数库。
函数arange (start, stop, step )
      np.arange(3,7,0.5)          #[3. 3.5 4. 4.5 5. 5.5 6. 6.5]
函数linspace (start,stop, number)
      np.linspace(-1,1, 5)        #[-1. , -0.5,  0. ,  0.5,  1. ]
sin()、cos()、sqrt()、log()……
常量pi
numpy库

图片对象数：1

## 第87页

Matplotlib常用函数
函数名称
函数作用
plt.title()
添加标题，可指定名称、位置、颜色、字体大小等
plt.xlabel()
添加x轴名称，可以指定位置、颜色、字体大小等
plt.ylabel()
添加y轴名称，可以指定位置、颜色、字体大小等
plt.xlim()
指定x轴的范围，确定一个数值区间
plt.ylim()
指定y轴的范围，确定一个数值区间
plt.xticks()
指定x轴刻度的数目与取值
plt.yticks()
指定y轴刻度的数目与取值
plt.legend()
指定图例，可以指定图例的大小、位置、标签

图片对象数：1

## 第88页

import matplotlib.pyplot as plt
import numpy as np
x=np.arange(0,1,0.01)
y= x**2 
plt.plot(x,y,’b’)
plt.plot(x,x**3)
Matplotlib折线图示例
plt.title('math example')
plt.xlim(0,1)
plt.ylim(0,1)
plt.ylabel('Y')
plt.xticks([0,0.25,0.5,0.75,1.0])
plt.legend(['y=x^2','y=x^3'])
plt.show()

图片对象数：2

## 第89页

课堂练习
      创建6*6的画布，以画布中心为原点画出坐标轴，并按以下公式绘制函数曲线（ 其中wh、hh的取值分别为画布的半宽和半高，t的取值范围为0至4π，100个采样点）。 
     x = (wh / 4) * (sin(2t) + 2 * cos(t))
     y = (hh / 4) * (cos(2t) + 2 * sin(t))

图片对象数：2

## 第90页

import matplotlib.pyplot as plt
from numpy import *
plt.figure(figsize=(6, 6))
wh = hh = 6/2
plt.plot([-3,3],[0,0],c='r')
plt.plot([0,0],[-3,3],c='r')
t = linspace(0, 4*pi, 100) x=(wh/4)*(sin(2*t)+2*cos(t))
y=(hh/4)*(cos(2*t)+2*sin(t))
plt.plot(x, y,c='b')
plt.show()
课堂练习
坐标轴：plot([x1,x2],[y1,y2])其中（x1,y1）是起点
       （x2,y2）是终点。

图片对象数：2

## 第91页

4  网络爬虫

图片对象数：1

## 第92页

网络爬虫
网络爬虫（又被称为网页蜘蛛，网络机器人）：是一种按照一定的规则自动地抓取万维网信息的程序或者脚本。
     第三方的requests模块，需要安装pip install requests
     结合正则表达式应用，可简单实现对静态网页信息的自动下载。

图片对象数：1

## 第93页

简单爬虫程序的基本步骤
获取网页源代码
根据关注目标所在链接的特点写出正则表达式
用正则表达式匹配获取目标链接
用循环结构遍历目标链接并自动下载信息

图片对象数：1

## 第94页

requests.get()方法
url：拟获取页面的url链接
params：url中的额外参数（字典或字节流格式），可选
r：Response对象，包含爬虫返回的内容
r=requests.get(url, params=None)

图片对象数：2

## 第95页

Response对象的属性
属性
说明
r.status_code
HTTP请求的返回状态，200表示连接成功，404表示失败
r.text
HTTP响应内容的字符串形式,即url对应的页面内容
r.content
HTTP响应内容的二进制形式
r.encoding
从HTTP header中猜测的响应内容编码方式
r.apparent_encoding
从内容中分析出的响应内容编码方式（备选）

图片对象数：1

## 第96页

re库
Python处理正则表达式的标准库是re（regular expression）。
     re模块主要方法：
compile(pattern[,flags])   #创建模式对象  flag的常见取值re.I：忽略大小写。
split(pattern,string[,maxsplit=0])
findall(pattern,string[,flags])   #以列表形式返回全部能匹配的子串

图片对象数：2

## 第97页

元字符
元字符
描述
\
将下一个字符标记为一个特殊字符、或一个原义字符。例如，‘n' 匹配字符n。‘\n' 匹配一个换行符。
*
匹配前面的子表达式零次、一次或多次。例如，zo* 能匹配 “z” 、"zo"以及 "zoo"
+
匹配前面的子表达式一次或多次。例如，'zo+' 能匹配 "zo" 以及 "zoo"，但不能匹配 "z"。
?
匹配前面的子表达式零次或一次。例如，"do(es)?" 可以匹配 "do" 或 "does" 。
.
匹配除换行符（\n、\r）之外的任何单个字符。要匹配包括 '\n' 在内的任何字符，请使用像"(.|\n)"的模式。
（）
界定一个整体或子模式
正则表达式是一种文本模式，包括普通字符（例如，a 到 z 之间的字母）和特殊字符

图片对象数：1

## 第98页

贪婪匹配
贪婪匹配是一种尽可能多地匹配字符的匹配模式
贪婪匹配是re库正则表达式默认的匹配方式，即输出匹配的最长的子串
用‘?‘使得’.*’采用非贪婪匹配（最小匹配）
>>> re.findall("ab.*c","abcbbbbbc")
['abcbbbbbc']
>>> re.findall("ab.*?c","abcbbbbbc")
['abc']

图片对象数：0

## 第99页

示例-代码

图片对象数：2

## 第100页

第8章  图形化界面设计

图片对象数：0

## 第101页

内容
 理解按钮、标签、输入框、文本框、单选按钮、复选框等可视化控件的功能。
 掌握tkinter控件的共同属性和特有属性。
 理解控件布局的三种方法。
 掌握几种常用控件在可视化程序设计中的设置和取值方法。
 学会用户事件响应与自定义函数绑定。

图片对象数：0

## 第102页


图片对象数：1

## 第103页

【例8-2】 标签及其常见属性示例
from tkinter import *
root=Tk()
lb=Label(root,text='我是一个标签',\
              bg='#d3fbfb',\
              fg='red',\
              font=('华文新魏',32),\
              width=20,\
              height=2,\
              relief=SUNKEN)
lb.pack()
root.mainloop()

图片对象数：1

## 第104页

【例8-4】 用pack()方法加参数排列标签
from tkinter import *
root = Tk()
 
lbred = Label(root, text="Red", fg="red",relief=GROOVE)
lbred.pack()
lbgreen = Label(root, text="绿色", fg="green",relief=GROOVE)
lbgreen.pack(side=RIGHT)
lbblue = Label(root, text="蓝", fg="blue",relief=GROOVE)
lbblue.pack(fill=X)
 
root.mainloop()
参数fill：可取值X\Y\BOTH，分别表示允许控件实例向水平、垂直或二维方向伸展填充父容器未被占用的空间
参数side：TOP\LEFT\RIGHT\BOTTOM，表示本控件相对于下一个控件实例的方位。

图片对象数：1

## 第105页

1．标签（Label）和消息（Message）
标签（Label）和消息（Message）除单行与多行不同外，属性与用法基本一致，用于呈现文本信息。
值得注意的是，属性text通常用于实例在第一次呈现时的固定文本，而如果需要在程序执行后发生变化，则可使用下列方法实现：
① 用控件实例的configure()方法改变属性text的值，可使显示的文本发生变化；

图片对象数：0

## 第106页

【例8-7】 制作一个电子时钟
>>>import time
>>>dir(time)
>>>help(time)

图片对象数：5

## 第107页

2．文本框

图片对象数：1

## 第108页

3．输入框
输入框（Entry）通常作为功能较为单一的接收单行文本输入的控件，虽然也有许多对其中文本进行操作的方法，但常用的只有取值方法get()和用于删除文本的delete(起始位置,终止位置)，例如，清空输入框为delete(0,END)。其应用实例，将结合后续控件展示。

图片对象数：0

## 第109页

8.2.2  按钮
按钮（Button）主要是为响应鼠标单击事件触发运行程序所设的，故其除控件共有属性外，属性command是最为重要的属性。
通常，将按钮要触发执行的程序以函数形式预先定义，然后可用以下两种方法调用函数。
① 直接调用函数。参数表达式为“command＝函数名”，注意函数名后面不要加括号，也不能传递参数。例如，例8-9中的command=run1。
② 利用匿名函数调用函数和传递参数。参数表达式为“command＝lambda:函数名(参数列表)”。
例如，例8-9中的“command=lambda:run2(inp1.get(),inp2.get())”

图片对象数：0

## 第110页

【例8-9】 简单加法器。
从两个输入框取得输入文本后转为浮点数值进行加法运算，要求每次单击按钮产生的算式结果以文本形式追加到文本框中，并将原输入框清空。
按钮“方法一”不传递参数调用函数run1()实现，按钮“方法二”用lambda调用函数run2(x,y)并同时传递参数实现(也可以增加：run3()使用bind方法实现)

图片对象数：2

## 第111页

谢         谢

图片对象数：1
