---
title: Python 速通 — 从变量到文件处理与正则
type: theory
tags: [python, programming, oop, file-io, regex, learning]
created: 2026-05-25
updated: 2026-05-26
source: raw/Python-100-Days/
---

# Python 速通 — 从变量到文件处理与正则

> 目标：能看懂代码、能写基础代码，不再依赖 AI 写代码。

---

## 一、速通学习路线（核心目标：不依赖 AI，能看懂能写）

> 按「7 天速通」设计，每天 2-3 小时，边学边练。
> **目标**：学完后能自己写代码处理数据、调用 API、做小工具

| 天 | 主题 | 原始章节 | 核心产出 | 实际应用场景 |
|----|------|----------|----------|--------------|
| D1 | 变量 + 运算 + 分支 | 03-05 | 能写条件判断逻辑 | 判断成绩、BMI计算 |
| D2 | 循环 + 列表基础 | 06,08-1 | 能写遍历/筛选逻辑 | 统计成绩、数据筛选 |
| D3 | 列表高级 + 元组 | 09,10 | 能操作集合数据 | 批量处理、抽奖程序 |
| D4 | 字符串 + 字典 | 11,13 | 能做文本处理和数据映射 | 日志分析、配置管理 |
| D5 | 函数 + 模块 | 14,16 | 能封装复用代码 | 封装工具函数 |
| D6 | 文件读写 + 异常 + 正则 | 21,30 | 能读写文件处理数据 | CSV数据处理、正则提取 |
| D7 | 实战综合 + 进阶 | 07,31 | 能独立完成小项目 | 数据清洗、数据库操作 |

**关键原则**：
- 每学完一个主题，**必须手写代码**验证，不懂再查文档
- 禁止直接复制 AI 生成的代码，必须自己写
- 遇到报错先自己排查 10 分钟，再求助

---

## 二、知识体系总览

```
基础语法（03-07）
    │
    ├── 变量与数据类型：int / float / str / bool
    ├── 运算符：算术 / 比较 / 逻辑 / 位运算
    ├── 分支结构：if / elif / else
    └── 循环结构：for-in / while / break / continue
          │
数据结构（08-13）
    │
    ├── 列表：可变有序序列，支持索引/切片/方法
    ├── 元组：不可变有序序列，打包解包
    ├── 字符串：不可变文本，切片/格式化/方法
    ├── 集合：无序不重复，支持数学运算
    └── 字典：键值对映射，字典生成式
          │
函数与模块（14-17）
    │
    ├── 函数定义：def / return / 参数类型
    ├── 模块使用：import / from...import
    ├── 高阶函数：函数作参数/返回值
    ├── Lambda：匿名函数
    ├── 装饰器：@decorator 语法糖
    └── 递归：函数调用自身
          │
面向对象（18-20）
    │
    ├── 类与对象：class / __init__ / self
    ├── 封装：私有属性 / @property
    ├── 继承：class Child(Parent)
    ├── 多态：同一方法不同实现
    └── 实战：扑克游戏 / 工资结算
          │
文件与数据处理（21-30）
    │
    ├── 文件读写：open / read / write / with 上下文
    ├── 异常处理：try / except / finally / raise / 自定义异常
    ├── 序列化：json / pickle / requests 调 API
    ├── CSV：csv.reader / csv.writer / pandas.read_csv
    ├── Excel：openpyxl 读写 xlsx / xlrd+xlwt 读写 xls
    ├── Office：python-docx / python-pptx 模板批量生成
    ├── PDF：PyPDF2 提取/加密/水印 / reportlab 创建
    ├── 图像：Pillow 打开/裁剪/滤镜/绘图 / OpenCV
    ├── 邮件/短信：smtplib + MIME / requests 调短信 API
    └── 正则表达式：元字符 / 量词 / 分组 / re 模块
          │
Python 进阶（31-60）
    │
    ├── 生成式/推导式：列表/集合/字典生成式
    ├──  itertools：排列/组合/笛卡尔积
    ├──  collections：Counter/ defaultdict/ deque
    ├──  heapq：堆排序，找出最大/最小N个元素
    ├──  算法复杂度：O(1)/O(log n)/O(n)/O(n log n)/O(n²)
    ├──  排序算法：选择/冒泡/归并/快速排序
    ├──  查找算法：顺序查找/二分查找
    ├──  MySQL操作：pymysql / 连接/游标/事务
    ├──  SQL基础：DQL/DML/DDL/DCL
└── 单元测试：unittest / pytest
          │
Python 高级应用（60-100）
    │
    ├── 网络爬虫：requests / BeautifulSoup / Scrapy
    ├── 并发编程：threading / multiprocessing / asyncio
    ├── 数据分析：NumPy / Pandas / Matplotlib
    ├── 机器学习：sklearn / 回归/分类/聚类
    ├── Web开发：Django / DRF / RESTful
    ├── Docker容器：镜像/容器/Compose
    └── 面试算法：剑指Offer/力扣高频题
```

---

## 二、核心知识点速查

### 2.1 变量与数据类型

| 类型 | 示例 | 特点 |
|------|------|------|
| int | `a = 42` | 整数，无大小限制 |
| float | `b = 3.14` | 浮点数 |
| str | `s = "hello"` | 不可变，支持切片 |
| bool | `flag = True` | True / False |
| list | `lst = [1, 2, 3]` | 可变有序 |
| tuple | `t = (1, 2)` | 不可变有序 |
| dict | `d = {"a": 1}` | 键值对 |
| set | `s = {1, 2, 3}` | 无序不重复 |

**类型转换**：`int()` / `float()` / `str()` / `list()` / `tuple()`

### 2.2 运算符优先级（从高到低）

```
() 括号
** 幂运算
+x, -x 正负号
*, /, //, % 乘除整除取余
+, - 加减
<<, >> 位移
& 按位与
^ 按位异或
| 按位或
<, <=, >, >=, ==, != 比较
not 逻辑非
and 逻辑与
or 逻辑或
```

### 2.3 分支与循环

**分支结构**：
```python
if condition1:
    # do something
elif condition2:
    # do another
else:
    # default
```

**循环结构**：
```python
# for-in 遍历
for item in iterable:
    # process item

# while 循环
while condition:
    # do something

# 控制语句
break   # 跳出循环
continue  # 跳过本次
```

### 2.4 列表核心方法

| 方法 | 作用 | 示例 |
|------|------|------|
| append(x) | 末尾添加 | `lst.append(4)` |
| insert(i, x) | 指定位置插入 | `lst.insert(0, 0)` |
| pop([i]) | 删除并返回 | `lst.pop()` |
| remove(x) | 删除第一个x | `lst.remove(2)` |
| sort() | 原地排序 | `lst.sort()` |
| reverse() | 原地反转 | `lst.reverse()` |
| index(x) | 返回索引 | `lst.index(3)` |
| count(x) | 统计次数 | `lst.count(2)` |

**切片语法**：`lst[start:stop:step]`

### 2.5 字符串格式化

```python
# f-string（推荐）
name = "张三"
age = 20
print(f"姓名：{name}，年龄：{age}")

# format 方法
print("姓名：{}，年龄：{}".format(name, age))

# % 格式化（旧）
print("姓名：%s，年龄：%d" % (name, age))
```

### 2.6 字典核心方法

| 方法 | 作用 |
|------|------|
| get(key, default) | 安全获取 |
| keys() / values() / items() | 视图对象 |
| update(d) | 合并字典 |
| pop(key) | 删除并返回 |

**字典生成式**：
```python
squares = {x: x**2 for x in range(1, 6)}
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

### 2.7 函数参数类型

```python
def func(
    pos,           # 位置参数
    *args,         # 可变位置参数（元组）
    keyword=value, # 默认参数
    **kwargs       # 可变关键字参数（字典）
):
    pass
```

### 2.8 高阶函数

```python
# map：对每个元素应用函数
list(map(lambda x: x**2, [1, 2, 3]))  # [1, 4, 9]

# filter：过滤满足条件的元素
list(filter(lambda x: x > 0, [-1, 0, 1, 2]))  # [1, 2]

# reduce：累积计算
from functools import reduce
reduce(lambda a, b: a + b, [1, 2, 3, 4])  # 10
```

### 2.9 装饰器模式

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        # 前置处理
        result = func(*args, **kwargs)
        # 后置处理
        return result
    return wrapper

@decorator
def my_func():
    pass
```

### 2.10 面向对象核心

```python
class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    def say_hello(self):
        print(f"Hello, I'm {self._name}")

class Student(Person):
    def __init__(self, name, age, grade):
        super().__init__(name, age)
        self.grade = grade
```

**OOP 三大特性**：封装（隐藏实现暴露接口） / 继承（复用父类） / 多态（同一接口不同实现）

### 2.11 文件读写与异常处理

```python
# with 上下文 + 异常处理（推荐写法）
try:
    with open('file.txt', 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print('文件不存在!')
```

| open 模式 | 含义 |
|-----------|------|
| `r` | 只读（默认） |
| `w` | 写入（截断） |
| `a` | 追加 |
| `b` | 二进制模式 |
| `rb` / `wb` | 二进制读写 |

**异常处理五关键字**：`try` → `except` → `else`（无异常时） → `finally`（始终执行） → `raise`（主动抛出）

```python
class InputError(ValueError):
    pass

def fac(num):
    if num < 0:
        raise InputError('只能计算非负整数阶乘')
```

### 2.12 序列化与 JSON

```python
import json

# 序列化到文件
with open('data.json', 'w') as f:
    json.dump(my_dict, f, ensure_ascii=False)

# 反序列化
with open('data.json', 'r') as f:
    data = json.load(f)

# 调网络 API 获取 JSON
import requests
resp = requests.get('http://api.example.com/data?key=xxx')
if resp.status_code == 200:
    data = resp.json()
```

| JSON 类型 | Python 类型 |
|-----------|-------------|
| object | dict |
| array | list |
| true/false | True/False |
| null | None |

其他方案：`pickle`（Python 专用，非跨语言）/ `shelve`（键值存储）

### 2.13 CSV 读写

```python
import csv

# 写入
with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['姓名', '语文', '数学'])
    writer.writerow(['关羽', 98, 86])

# 读取
with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)  # row 是列表
```

更强替代：`pd.read_csv()` → DataFrame，支持清洗/转换/聚合。

### 2.14 Excel 读写（openpyxl）

```python
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment

wb = load_workbook('data.xlsx')
sheet = wb.worksheets[0]
sheet['E1'] = '平均分'
sheet.cell(1, 5).font = Font(size=18, bold=True)
sheet['E2'] = '=average(B2:D2)'
wb.save('output.xlsx')
```

旧版 `.xls` 用 `xlrd` 读 + `xlwt` 写；新版 `.xlsx` 用 `openpyxl` 可同时读写。

### 2.15 Office 文档操作

**Word 模板批量生成**（核心模式）：
```python
from docx import Document
for emp in employees:
    doc = Document('模板.docx')
    for p in doc.paragraphs:
        for run in p.runs:
            if '{' in run.text:
                key = run.text[run.text.find('{')+1:run.text.find('}')]
                run.text = run.text.replace('{'+key+'}', emp[key])
    doc.save(f'{emp["name"]}离职证明.docx')
```

**PPT 创建**：`Presentation()` → `add_slide()` → `shapes.title.text` → `save()`

### 2.16 PDF 操作

```python
# 批量添加水印
import PyPDF2
reader = PyPDF2.PdfReader('doc.pdf')
watermark = PyPDF2.PdfReader('watermark.pdf').pages[0]
writer = PyPDF2.PdfWriter()
for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)
with open('output.pdf', 'wb') as f:
    writer.write(f)
```

创建 PDF 用 `reportlab`：`Canvas` + `drawString` + `setFont`（中文需 `registerFont`）

### 2.17 图像处理（Pillow）

```python
from PIL import Image, ImageFilter, ImageDraw

img = Image.open('photo.jpg')
img.crop((80, 20, 310, 360))       # 剪裁
img.thumbnail((128, 128))           # 缩略图
img.rotate(45)                      # 旋转
img.filter(ImageFilter.CONTOUR)     # 轮廓滤镜

# 绘图
draw = ImageDraw.Draw(img)
draw.rectangle([100, 100, 300, 300], outline='red', width=2)
```

### 2.18 邮件发送

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email = MIMEMultipart()
email['From'], email['To'], email['Subject'] = from_u, to_u, subj
email.attach(MIMEText(content, 'html', 'utf-8'))

smtp = smtplib.SMTP_SSL('smtp.126.com', 465)
smtp.login(USER, AUTH_CODE)  # 授权码，非密码
smtp.sendmail(from_u, [to_u], email.as_string())
```

### 2.19 正则表达式

| 元字符 | 含义 | 量词 | 含义 |
|--------|------|------|------|
| `\d` | 数字 | `*` | 0+次 |
| `\w` | 字母数字下划线 | `+` | 1+次 |
| `\s` | 空白 | `?` | 0或1次 |
| `.` | 任意字符 | `{M,N}` | M到N次 |
| `^` / `$` | 开头/结尾 | `*?` | 非贪婪 |

```python
import re
re.match(r'^\w{6,20}$', username)          # 验证格式
re.findall(r'1[34578]\d{9}', text)          # 提取手机号
re.sub(r'badword', '*', text, flags=re.I)   # 替换敏感词
re.split(r'[，。]', poem)                    # 按标点拆分

pattern = re.compile(r'(?<=\D)1[3-9]\d{9}(?=\D)')  # 预编译复用
```

### 2.20 Python 进阶：生成式与推导式

```python
# 列表生成式
squares = [x**2 for x in range(1, 6)]  # [1, 4, 9, 16, 25]

# 带条件过滤
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]

# 字典生成式
prices = {'A': 100, 'B': 200, 'C': 150}
expensive = {k: v for k, v in prices.items() if v > 100}  # {'B': 200}

# 集合生成式
squares_set = {x**2 for x in range(5)}  # {0, 1, 4, 9, 16}
```

### 2.21 itertools 模块（排列组合）

```python
import itertools

# 全排列
list(itertools.permutations('ABC'))  # [('A','B','C'), ...]

# 组合（五选三）
list(itertools.combinations('ABCDE', 3))  # [('A','B','C'), ...]

# 笛卡尔积
list(itertools.product('AB', '12'))  # [('A','1'), ('A','2'), ('B','1'), ('B','2')]

# 无限循环
cycle = itertools.cycle([1, 2, 3])
```

### 2.22 collections 模块（计数器、双端队列）

```python
from collections import Counter, defaultdict, deque

# Counter：统计元素出现次数
words = ['a', 'b', 'a', 'c', 'b', 'a']
counter = Counter(words)
print(counter.most_common(2))  # [('a', 3), ('b', 2)]

# defaultdict：带默认值的字典
dd = defaultdict(list)
dd['fruits'].append('apple')
print(dd)  # {'fruits': ['apple']}

# deque：双端队列（头尾操作高效）
dq = deque([1, 2, 3])
dq.appendleft(0)  # 头部插入
dq.append(4)      # 尾部插入
print(dq)  # deque([0, 1, 2, 3, 4])
```

### 2.23 heapq（堆排序）

```python
import heapq

nums = [34, 25, 12, 99, 87, 63, 58]
print(heapq.nlargest(3, nums))   # [99, 87, 63] - 最大3个
print(heapq.nsmallest(3, nums))  # [12, 25, 34] - 最小3个

# 带key排序
people = [{'name': 'A', 'age': 30}, {'name': 'B', 'age': 20}]
print(heapq.nlargest(2, people, key=lambda x: x['age']))
```

### 2.24 算法复杂度速查

| 复杂度 | 名称 | 例子 |
|--------|------|------|
| O(1) | 常量时间 | 哈希表访问 |
| O(log n) | 对数时间 | 二分查找 |
| O(n) | 线性时间 | 顺序遍历 |
| O(n log n) | 对数线性 | 快速排序/归并排序 |
| O(n²) | 平方时间 | 冒泡排序/选择排序 |

### 2.25 常见排序算法实现

```python
# 选择排序
def select_sort(items):
    items = items[:]
    for i in range(len(items)-1):
        min_idx = i
        for j in range(i+1, len(items)):
            if items[j] < items[min_idx]:
                min_idx = j
        items[i], items[min_idx] = items[min_idx], items[i]
    return items

# 冒泡排序（优化版）
def bubble_sort(items):
    items = items[:]
    for i in range(len(items)-1):
        swapped = False
        for j in range(len(items)-1-i):
            if items[j] > items[j+1]:
                items[j], items[j+1] = items[j+1], items[j]
                swapped = True
        if not swapped:
            break
    return items

# 二分查找（前提：有序列表）
def binary_search(items, target):
    left, right = 0, len(items) - 1
    while left <= right:
        mid = (left + right) // 2
        if items[mid] == target:
            return mid
        elif items[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

### 2.26 MySQL 数据库操作（pymysql）

```python
import pymysql

# 连接数据库
conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='password',
    database='test_db',
    charset='utf8mb4'
)

# 插入数据
with conn.cursor() as cursor:
    cursor.execute('INSERT INTO users (name, age) VALUES (%s, %s)', ('张三', 20))
    conn.commit()

# 查询数据
with conn.cursor() as cursor:
    cursor.execute('SELECT * FROM users WHERE age > %s', (18,))
    results = cursor.fetchall()
    for row in results:
        print(row)

conn.close()
```

### 2.27 正则表达式（进阶）

```python
import re

# 验证手机号
phone = re.match(r'^1[3-9]\d{9}$', '13812345678')

# 提取所有手机号
text = '我的手机是13812345678，还有13998765432'
phones = re.findall(r'1[3-9]\d{9}', text)

# 提取邮箱
email = re.findall(r'[\w.-]+@[\w.-]+\.\w+', 'test@example.com')

# 替换敏感词
text = re.sub(r'(fuck|shit)', '***', text, flags=re.I)

# 按分隔符拆分
parts = re.split(r'[,\s;]+', 'a,b;c d')

# 预编译正则（重复使用时更高效）
pattern = re.compile(r'(?<=\D)1[3-9]\d{9}(?=\D)')
result = pattern.findall(text)
```

### 2.28 单元测试（unittest）

```python
import unittest

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1 + 1, 2)
    
    def test_divide(self):
        self.assertRaises(ZeroDivisionError, lambda: 1 / 0)

if __name__ == '__main__':
    unittest.main()
```

---

## 三、避坑提醒（速通核心）

### 3.1 速通学习原则
```python
# ❌ 错误做法
1. 遇到问题就问 AI
2. 直接复制代码不调试
3. 看懂就等于会了

# ✅ 正确做法
1. 先自己写，不管对错
2. 报错自己排查 10 分钟
3. 必须手敲代码，不能复制
4. 遇到问题先看报错信息，再查文档
```

### 3.2 常见报错速查
```python
# SyntaxError: invalid syntax
# → 语法错误，检查缩进、括号、引号、冒号

# NameError: name 'xxx' is not defined
# → 变量未定义，检查变量名拼写

# IndentationError: unexpected indent
# → 缩进错误，Python 用缩进表示代码块

# TypeError: unsupported operand type(s)
# → 类型错误，字符串不能用 + 拼接数字

# IndexError: list index out of range
# → 索引越界，列表/字符串索引从 0 开始

# FileNotFoundError: [Errno 2] No such file or directory
# → 文件路径错误，检查文件是否存在
```

### 3.3 可变默认参数陷阱

```python
# 错误：默认参数在函数定义时创建，会被复用
def add_item(item, lst=[]):
    lst.append(item)
    return lst

# 正确：使用 None 作为默认值
def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

### 3.2 循环中修改列表

```python
# 错误：遍历时删除元素
for item in lst:
    if condition:
        lst.remove(item)

# 正确：遍历副本或使用列表生成式
lst = [x for x in lst if not condition(x)]
```

### 3.3 浮点数比较

```python
# 错误：直接比较
0.1 + 0.2 == 0.3  # False

# 正确：使用容差
abs(0.1 + 0.2 - 0.3) < 1e-9  # True
```

### 3.4 浅拷贝 vs 深拷贝

```python
import copy

lst = [[1, 2], [3, 4]]
shallow = lst[:]  # 或 lst.copy()
deep = copy.deepcopy(lst)

# 浅拷贝：嵌套列表共享引用
# 深拷贝：完全独立
```

### 3.5 with 忘写导致文件未关闭

```python
# 错误：忘记 close，文件锁未释放
f = open('data.txt', 'w')
f.write('hello')

# 正确：用 with 自动关闭
with open('data.txt', 'w') as f:
    f.write('hello')
```

### 3.6 JSON 中文变 \uXXXX

```python
# 错误：中文被 Unicode 转义
json.dumps({"名": "张三"})  # '{"\\u540d": "\\u5f20\\u4e09"}'

# 正确：加 ensure_ascii=False
json.dumps({"名": "张三"}, ensure_ascii=False)  # '{"名": "张三"}'
```

### 3.7 正则表达式忘写 r 前缀

```python
# 错误：\d 被Python解释为转义字符
re.match('\d+', '123')  # 可能出错

# 正确：用原始字符串
re.match(r'\d+', '123')
```

### 3.8 装饰器丢函数元信息

```python
from functools import wraps

def decorator(func):
    @wraps(func)  # 不加则原函数名/文档丢失
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

## 四、学习进度（每日打卡）

| 天 | 章节 | 内容 | 状态 | 掌握程度 | 打卡 |
|----|------|------|------|----------|------|
| D1 | 03-04 | 变量与运算符 | 待学习 | - | [ ] |
| D1 | 05 | 分支结构 | 待学习 | - | [ ] |
| D2 | 06 | 循环结构 | 待学习 | - | [ ] |
| D2 | 08-1 | 列表基础 | 待学习 | - | [ ] |
| D3 | 09 | 列表方法 | 待学习 | - | [ ] |
| D3 | 10 | 元组与打包解包 | 待学习 | - | [ ] |
| D4 | 11 | 字符串 | 待学习 | - | [ ] |
| D4 | 13 | 字典 | 待学习 | - | [ ] |
| D5 | 14 | 函数定义 | 待学习 | - | [ ] |
| D5 | 16 | 模块与包 | 待学习 | - | [ ] |
| D6 | 21 | 文件读写 | 待学习 | - | [ ] |
| D6 | 22 | 序列化与JSON | 待学习 | - | [ ] |
| D7 | 07+30 | 实战+正则 | 待学习 | - | [ ] |

---

## 五、实践任务

**基础（D1-D3）**：
- [ ] 用分支结构实现成绩等级判定
- [ ] 用循环打印九九乘法表
- [ ] 用列表实现学生成绩管理
- [ ] 用字典统计单词出现次数

**进阶（D4）**：
- [ ] 用函数实现计算器功能
- [ ] 用面向对象设计一个简单的图书管理系统

**实战（D5）**：
- [ ] 读取 CSV 文件统计平均分并写入新 Excel
- [ ] 用正则从日志文件中提取所有手机号和邮箱
- [ ] 批量生成 10 份带占位符的 Word 文档
- [ ] 给 PDF 批量添加水印

---

## 六、费曼检验问题

1. 为什么 Python 的整数没有大小限制？底层是如何实现的？
2. 列表的 `+=` 操作和 `extend()` 方法有什么区别？
3. 装饰器的本质是什么？`@decorator` 语法糖等价于什么代码？
4. `with open(...) as f` 做了什么？为什么不需要手动 `close()`？
5. JSON 和 pickle 序列化各有什么适用场景？为什么不推荐用 pickle 做跨语言数据交换？
6. 正则中贪婪和非贪婪匹配有什么区别？`.*?` 和 `.*` 分别匹配什么？

---

## 五、网络数据采集（62章）

### 5.1 requests 库

```python
import requests

# GET 请求
resp = requests.get('https://api.example.com/data')
if resp.status_code == 200:
    print(resp.json())  # 解析 JSON 响应
    print(resp.text)    # 获取文本内容
    print(resp.content) # 获取二进制内容

# POST 请求（带参数）
resp = requests.post('https://api.example.com/login', 
                     data={'username': 'admin', 'password': '123'})
print(resp.json())

# 设置请求头
headers = {'User-Agent': 'Mozilla/5.0'}
resp = requests.get('https://example.com', headers=headers)

# 超时设置
resp = requests.get('https://example.com', timeout=10)
```

### 5.2 BeautifulSoup 解析 HTML

```python
from bs4 import BeautifulSoup

html = '''
<html><body>
    <a href="/page1" class="article">文章1</a>
    <a href="/page2" class="article">文章2</a>
</body></html>
'''

soup = BeautifulSoup(html, 'html.parser')

# 按标签查找
links = soup.find_all('a', class_='article')
for link in links:
    print(link.get('href'), link.text)

# CSS 选择器
titles = soup.select('.article')
```

### 5.3 爬虫实战（豆瓣电影Top250）

```python
import re
import requests
from bs4 import BeautifulSoup

def get_movies(start=0):
    url = f'https://movie.douban.com/top250?start={start}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    movies = []
    for item in soup.select('div.item'):
        title = item.select_one('span.title').text
        rating = item.select_one('span.rating_num').text
        movies.append({'title': title, 'rating': rating})
    return movies

# 获取全部250部电影
all_movies = []
for i in range(0, 250, 25):
    all_movies.extend(get_movies(i))
```

---

## 六、并发编程（63章）

### 6.1 多线程 threading

```python
import threading
import time

def download(filename):
    print(f'开始下载 {filename}')
    time.sleep(2)  # 模拟下载
    print(f'{filename} 下载完成')

# 创建线程
t1 = threading.Thread(target=download, args=('a.mp4',))
t2 = threading.Thread(target=download, args=('b.mp4',))

t1.start()
t2.start()
t1.join()  # 等待线程结束
t2.join()
print('全部完成')
```

### 6.2 多进程 multiprocessing

```python
from multiprocessing import Process

def worker(num):
    print(f'进程 {num} 开始工作')

if __name__ == '__main__':
    for i in range(4):
        p = Process(target=worker, args=(i,))
        p.start()
```

### 6.3 异步 asyncio

```python
import asyncio

async def fetch(url):
    print(f'获取 {url}')
    await asyncio.sleep(1)  # 模拟网络请求
    return f'{url} 数据'

async def main():
    results = await asyncio.gather(
        fetch('a.com'),
        fetch('b.com'),
        fetch('c.com')
    )
    print(results)

asyncio.run(main())
```

---

## 七、数据分析基础（66-80章）

### 7.1 NumPy 核心操作

```python
import numpy as np

# 创建数组
arr = np.array([1, 2, 3, 4, 5])
arr2d = np.array([[1, 2, 3], [4, 5, 6]])

# 基础运算
print(arr * 2)      # 每个元素乘2
print(arr.sum())    # 求和
print(arr.mean())   # 平均值
print(arr.max())    # 最大值

# 数组切片
print(arr2d[0, :])  # 第一行
print(arr2d[:, 1])  # 第二列

# 条件筛选
arr = np.array([1, 2, 3, 4, 5])
print(arr[arr > 3])  # [4, 5]
```

### 7.2 Pandas 核心操作

```python
import pandas as pd

# 创建 DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'score': [85, 90, 78]
})

# 读取文件
df = pd.read_csv('data.csv')
df = pd.read_excel('data.xlsx')

# 基础操作
print(df.head())     # 前5行
print(df.shape)      # 行数列数
print(df.columns)    # 列名
print(df.dtypes)     # 数据类型

# 筛选过滤
print(df[df['age'] > 25])              # 按条件过滤
print(df[df['name'].str.contains('A')])  # 字符串包含

# 分组聚合
print(df.groupby('dept')['salary'].mean())

# 排序
df = df.sort_values('score', ascending=False)
```

### 7.3 Matplotlib 可视化

```python
import matplotlib.pyplot as plt

# 折线图
plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
plt.title('折线图')
plt.xlabel('X轴')
plt.ylabel('Y轴')
plt.show()

# 柱状图
plt.bar(['A', 'B', 'C'], [10, 20, 15])
plt.show()

# 散点图
plt.scatter([1, 2, 3], [3, 6, 9])
plt.show()
```

---

## 八、面试算法速刷

### 8.1 剑指Offer高频题

| 题目 | 难度 | 核心思路 |
|------|------|----------|
| 两数之和 | ⭐ | 哈希表 / 暴力 |
| 反转链表 | ⭐ | 双指针 / 递归 |
| 斐波那契数列 | ⭐ | 动态规划 / 递归 |
| 二维数组查找 | ⭐⭐ | 从右上角开始二分 |
| 替换空格 | ⭐ | 字符串遍历 |
| 栈实现队列 | ⭐⭐ | 双栈 |
| 旋转数组最小数字 | ⭐⭐ | 二分查找 |
| 跳台阶 | ⭐⭐ | 动态规划 |

### 8.2 刷题策略

```python
# 数组类
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i
    return []

# 链表类（反转链表）
def reverse_list(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev

# 字符串类（回文判断）
def is_palindrome(s):
    s = ''.join(c.lower() for c in s if c.isalnum())
    return s == s[::-1]
```

---

## 九、Python 常见坑与最佳实践

### 9.1 整数比较的坑

```python
# is 比较的是对象id，== 比较的是对象内容
a = 257
b = 257
print(a is b)   # False（CPython缓存范围是 -5~256）
print(a == b)   # True

# 小整数在缓存范围内
x = 5
y = 5
print(x is y)   # True
```

### 9.2 可变默认参数陷阱

```python
# 错误：默认参数在函数定义时创建，会被复用
def add_item(item, lst=[]):
    lst.append(item)
    return lst

# 正确：使用 None 作为默认值
def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

### 9.3 循环中修改列表

```python
# 错误：遍历时删除元素
for item in lst:
    if condition:
        lst.remove(item)

# 正确：遍历副本或使用列表生成式
lst = [x for x in lst if not condition(x)]
```

### 9.4 协程与异步

```python
import asyncio

# 协程函数
async def fetch(url):
    print(f'开始获取 {url}')
    await asyncio.sleep(1)  # 模拟异步操作
    return f'{url} 数据'

# 运行协程
async def main():
    result = await fetch('example.com')
    print(result)

asyncio.run(main())
```

---

## 十、代码风格与最佳实践

### 10.1 PEP8 风格指南要点

```python
# 1. 缩进：4个空格
if x > 0:
    print('positive')

# 2. 行长度：最大79字符
# 3. 空行：类和函数之间两个空行
# 4. 命名：
#   - 函数/变量：snake_case
#   - 类名：CapWords
#   - 常量：UPPER_CASE

# 5. 导入顺序：标准库 → 第三方 → 本地
import os
import sys

import requests
from mymodule import my_func
```

### 10.2 高效代码原则

```python
# 1. 使用内置函数和列表生成式
# 差
result = []
for x in items:
    result.append(x * 2)

# 好
result = [x * 2 for x in items]

# 2. 使用生成器节省内存
# 差：一次性加载
total = sum([x**2 for x in range(1000000)])

# 好：惰性计算
total = sum(x**2 for x in range(1000000))

# 3. 使用集合查找
# 差：O(n)
if item in items_list:

# 好：O(1)
if item in items_set:

# 4. 多用 dict/get 而非 try-except
# 差
try:
    value = d[key]
except KeyError:
    value = default

# 好
value = d.get(key, default)
```

---

## 十一、Pandas 数据分析快速参考

### 11.1 核心数据结构

```python
import pandas as pd
import numpy as np

# Series：一维带标签数组
s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])

# DataFrame：二维表格
df = pd.DataFrame({
    'name': ['Alice', 'Bob'],
    'age': [25, 30],
    'score': [85.5, 90.0]
})
```

### 11.2 数据加载

```python
# CSV
df = pd.read_csv('file.csv', encoding='utf-8')

# Excel
df = pd.read_excel('file.xlsx', sheet_name='Sheet1')

# 读取大文件（分块）
for chunk in pd.read_csv('big.csv', chunksize=10000):
    process(chunk)
```

### 11.3 数据清洗

```python
# 缺失值处理
df.dropna()              # 删除含缺失值的行
df.fillna(0)             # 用0填充缺失值
df.fillna(method='ffill') # 前向填充

# 去重
df.drop_duplicates(subset=['col1'])

# 数据类型转换
df['date'] = pd.to_datetime(df['date'])
df['age'] = df['age'].astype(int)
```

### 11.4 数据筛选与变换

```python
# 筛选
df[df['age'] > 25]                    # 条件筛选
df.query('age > 25 and score > 80')  # 查询语法

# 选择列
df[['name', 'score']]
df.loc[:, 'name':'score']            # 标签索引
df.iloc[:, 0:2]                      # 位置索引

# 新增列
df['total'] = df['score'] * 0.3 + df['age'] * 0.7

# 分组聚合
df.groupby('dept')['salary'].agg(['mean', 'sum', 'count'])
```

### 11.5 数据透视与连接

```python
# 透视表
pd.pivot_table(df, values='salary', index='dept', columns='year', aggfunc='sum')

# 连接
pd.merge(df1, df2, on='id', how='inner')  # 内连接
pd.concat([df1, df2], axis=0)               # 垂直拼接
```

---

## References

- [[wiki/my-learning-path/theory/python-drills|Python 速通练习]]
- [[wiki/sources/python-03-变量和数据类型.md|变量和数据类型]]
- [[wiki/sources/python-05-分支结构.md|分支结构]]
- [[wiki/sources/python-06-循环结构.md|循环结构]]
- [[wiki/sources/python-08-列表基础.md|列表基础]]
- [[wiki/sources/python-11-字符串.md|字符串]]
- [[wiki/sources/python-13-字典.md|字典]]
- [[wiki/sources/python-14-函数和模块.md|函数和模块]]
- [[wiki/sources/python-18-面向对象入门.md|面向对象入门]]
- [[wiki/concepts/python-面向对象.md|面向对象概念]]
- [[wiki/my-learning-path/theory/index|理论补全]]
