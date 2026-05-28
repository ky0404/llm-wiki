---
title: Python 速通练习
type: theory
tags: [python, practice, drills, learning]
created: 2026-05-26
updated: 2026-05-26
source: raw/Python-100-Days/
---

# Python 速通练习

> 配合 [[wiki/my-learning-path/theory/python-foundation|Python 速通]] 使用，每个主题 5 道题，从易到难。
> 规则：先手写代码，跑不通再查文档，禁止直接问 AI 要答案。

---

## D1：变量 + 运算 + 分支

### 1.1 温度转换

输入摄氏温度，输出华氏温度。公式：`F = C * 9 / 5 + 32`

<details>
<summary>参考答案</summary>

```python
c = float(input('请输入摄氏温度: '))
f = c * 9 / 5 + 32
print(f'华氏温度: {f:.1f}')
```

</details>

### 1.2 成绩等级判定

输入 0-100 分数，输出等级：90+ 为 A，80+ 为 B，70+ 为 C，60+ 为 D，否则 E。

<details>
<summary>参考答案</summary>

```python
score = int(input('请输入分数: '))
if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
elif score >= 60:
    grade = 'D'
else:
    grade = 'E'
print(f'等级: {grade}')
```

</details>

### 1.3 闰年判断

输入年份，判断是否为闰年。规则：能被4整除且不能被100整除，或能被400整除。

<details>
<summary>参考答案</summary>

```python
year = int(input('请输入年份: '))
is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
print(f'{year}年是{"闰年" if is_leap else "平年"}')
```

</details>

### 1.4 BMI 计算

输入身高(m)和体重(kg)，计算 BMI 并分类：<18.5 偏瘦、18.5-24 正常、24-28 偏胖、>=28 肥胖。

<details>
<summary>参考答案</summary>

```python
height = float(input('身高(m): '))
weight = float(input('体重(kg): '))
bmi = weight / height ** 2
if bmi < 18.5:
    cat = '偏瘦'
elif bmi < 24:
    cat = '正常'
elif bmi < 28:
    cat = '偏胖'
else:
    cat = '肥胖'
print(f'BMI: {bmi:.1f}, {cat}')
```

</details>

### 1.5 简易计算器

输入两个数和运算符(+ - * /)，输出结果。除数为0时提示错误。

<details>
<summary>参考答案</summary>

```python
a = float(input('第一个数: '))
op = input('运算符(+ - * /): ')
b = float(input('第二个数: '))

if op == '+':
    print(f'{a} + {b} = {a + b}')
elif op == '-':
    print(f'{a} - {b} = {a - b}')
elif op == '*':
    print(f'{a} * {b} = {a * b}')
elif op == '/':
    if b == 0:
        print('错误：除数不能为0')
    else:
        print(f'{a} / {b} = {a / b}')
else:
    print('不支持的运算符')
```

</details>

---

## D2：循环 + 列表 + 元组

### 2.1 九九乘法表

用循环打印九九乘法表。

<details>
<summary>参考答案</summary>

```python
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f'{j}x{i}={i*j}', end='\t')
    print()
```

</details>

### 2.2 猜数字游戏

程序随机生成 1-100 的数，用户猜，提示偏大/偏小，直到猜对，输出次数。

<details>
<summary>参考答案</summary>

```python
import random
target = random.randint(1, 100)
count = 0
while True:
    guess = int(input('猜一个数(1-100): '))
    count += 1
    if guess > target:
        print('偏大')
    elif guess < target:
        print('偏小')
    else:
        print(f'猜对了！共猜了{count}次')
        break
```

</details>

### 2.3 列表去重排序

输入一组数（逗号分隔），去重后升序输出。

<details>
<summary>参考答案</summary>

```python
nums = input('输入数字(逗号分隔): ')
lst = [int(x.strip()) for x in nums.split(',')]
result = sorted(set(lst))
print(result)
```

</details>

### 2.4 列表筛选

给定列表 `[1, -2, 3, -4, 5, -6, 7, 8, -9, 10]`，分别输出正数列表、负数列表、正数之和。

<details>
<summary>参考答案</summary>

```python
lst = [1, -2, 3, -4, 5, -6, 7, 8, -9, 10]
positives = [x for x in lst if x > 0]
negatives = [x for x in lst if x < 0]
print(f'正数: {positives}, 负数: {negatives}, 正数之和: {sum(positives)}')
```

</details>

### 2.5 冒泡排序

手写冒泡排序函数，对列表升序排列。

<details>
<summary>参考答案</summary>

```python
def bubble_sort(lst):
    arr = lst[:]
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

print(bubble_sort([5, 3, 8, 1, 9, 2]))
```

</details>

---

## D3：字符串 + 集合 + 字典

### 3.1 回文判断

输入字符串，判断是否为回文（忽略空格和大小写）。

<details>
<summary>参考答案</summary>

```python
s = input('输入字符串: ').replace(' ', '').lower()
print('是回文' if s == s[::-1] else '不是回文')
```

</details>

### 3.2 字符统计

输入字符串，统计每个字符出现次数，按次数降序输出。

<details>
<summary>参考答案</summary>

```python
s = input('输入字符串: ')
counter = {}
for ch in s:
    counter[ch] = counter.get(ch, 0) + 1
for ch, cnt in sorted(counter.items(), key=lambda x: x[1], reverse=True):
    print(f"'{ch}': {cnt}")
```

</details>

### 3.3 单词频率统计

输入英文句子，统计每个单词出现次数（忽略大小写和标点）。

<details>
<summary>参考答案</summary>

```python
import re
text = input('输入英文: ').lower()
words = re.findall(r'\b[a-z]+\b', text)
freq = {}
for w in words:
    freq[w] = freq.get(w, 0) + 1
print(freq)
```

</details>

### 3.4 两个集合运算

给定两个集合 A={1,2,3,4,5}, B={3,4,5,6,7}，输出交集、并集、差集(A-B)、对称差。

<details>
<summary>参考答案</summary>

```python
a = {1, 2, 3, 4, 5}
b = {3, 4, 5, 6, 7}
print(f'交集: {a & b}')
print(f'并集: {a | b}')
print(f'差集: {a - b}')
print(f'对称差: {a ^ b}')
```

</details>

### 3.5 学生成绩管理

用字典嵌套管理3个学生的3门课成绩，计算每人平均分和每科最高分。

<details>
<summary>参考答案</summary>

```python
students = {
    '张三': {'语文': 85, '数学': 92, '英语': 78},
    '李四': {'语文': 90, '数学': 88, '英语': 95},
    '王五': {'语文': 76, '数学': 95, '英语': 82},
}

for name, scores in students.items():
    avg = sum(scores.values()) / len(scores)
    print(f'{name} 平均分: {avg:.1f}')

for subject in ['语文', '数学', '英语']:
    top = max(students[s][subject] for s in students)
    print(f'{subject} 最高分: {top}')
```

</details>

---

## D4：函数 + 面向对象

### 4.1 递归求阶乘

写递归函数 `factorial(n)`，处理负数输入的异常。

<details>
<summary>参考答案</summary>

```python
def factorial(n):
    if n < 0:
        raise ValueError('负数没有阶乘')
    if n <= 1:
        return 1
    return n * factorial(n - 1)

try:
    print(factorial(int(input('输入非负整数: '))))
except ValueError as e:
    print(e)
```

</details>

### 4.2 可变参数函数

写函数 `make_profile(name, *hobbies, **details)`，输出姓名、爱好列表、详情字典。

<details>
<summary>参考答案</summary>

```python
def make_profile(name, *hobbies, **details):
    print(f'姓名: {name}')
    print(f'爱好: {list(hobbies)}')
    print(f'详情: {details}')

make_profile('张三', '编程', '游泳', age=22, city='广州')
```

</details>

### 4.3 装饰器计时

写装饰器 `@timer`，打印被装饰函数的执行时间。

<details>
<summary>参考答案</summary>

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        cost = time.time() - start
        print(f'{func.__name__} 执行耗时: {cost:.4f}s')
        return result
    return wrapper

@timer
def slow_add(a, b):
    time.sleep(0.1)
    return a + b

print(slow_add(1, 2))
```

</details>

### 4.4 简单图书类

定义 `Book` 类（书名、作者、价格），`@property` 控制价格不为负，实现 `__str__`。

<details>
<summary>参考答案</summary>

```python
class Book:
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError('价格不能为负')
        self._price = value

    def __str__(self):
        return f'《{self.title}》{self.author} ¥{self.price}'

b = Book('Python入门', '骆昊', 59.9)
print(b)
```

</details>

### 4.5 继承：员工与工资

`Employee` 基类（姓名、基本工资），`Manager` 子类（加津贴），`Developer` 子类（加项目奖金），各自实现 `calc_salary()`。

<details>
<summary>参考答案</summary>

```python
class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def calc_salary(self):
        return self.base_salary

class Manager(Employee):
    def __init__(self, name, base_salary, allowance):
        super().__init__(name, base_salary)
        self.allowance = allowance

    def calc_salary(self):
        return self.base_salary + self.allowance

class Developer(Employee):
    def __init__(self, name, base_salary, bonus):
        super().__init__(name, base_salary)
        self.bonus = bonus

    def calc_salary(self):
        return self.base_salary + self.bonus

for emp in [Manager('张三', 10000, 3000), Developer('李四', 12000, 5000)]:
    print(f'{emp.name} 工资: {emp.calc_salary()}')
```

</details>

---

## D5：文件 + 异常 + 序列化 + 正则

### 5.1 读写文本文件

写函数，将列表中每行字符串写入文件，再读回打印。

<details>
<summary>参考答案</summary>

```python
def write_and_read(lines, filename='test.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            print(line.rstrip())

write_and_read(['第一行', '第二行', '第三行'])
```

</details>

### 5.2 JSON 序列化学生数据

将字典列表序列化到 JSON 文件，再反序列化打印。

<details>
<summary>参考答案</summary>

```python
import json

students = [
    {'name': '张三', 'score': 85},
    {'name': '李四', 'score': 92},
]

with open('students.json', 'w', encoding='utf-8') as f:
    json.dump(students, f, ensure_ascii=False, indent=2)

with open('students.json', 'r', encoding='utf-8') as f:
    loaded = json.load(f)

for s in loaded:
    print(f"{s['name']}: {s['score']}")
```

</details>

### 5.3 CSV 读取统计

读取 CSV 文件（姓名,语文,数学,英语），计算每人平均分写入新 CSV。

<details>
<summary>参考答案</summary>

```python
import csv

with open('scores.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)

with open('averages.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header + ['平均分'])
    for row in rows:
        name = row[0]
        scores = [int(x) for x in row[1:]]
        avg = sum(scores) / len(scores)
        writer.writerow(row + [f'{avg:.1f}'])
```

</details>

### 5.4 正则提取信息

从日志文本中提取所有手机号和邮箱地址。

<details>
<summary>参考答案</summary>

```python
import re

log_text = """
用户13800138000于2026-01-01注册，邮箱zhang@test.com
用户15999887766于2026-02-15登录，邮箱li@demo.cn
"""

phones = re.findall(r'1[3-9]\d{9}', log_text)
emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+', log_text)
print(f'手机号: {phones}')
print(f'邮箱: {emails}')
```

</details>

### 5.5 综合实战：通讯录管理

写一个命令行通讯录：支持添加、删除、查询、保存到 JSON、从 JSON 加载。

<details>
<summary>参考答案</summary>

```python
import json
import os

FILE = 'contacts.json'

def load():
    if os.path.exists(FILE):
        with open(FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save(contacts):
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)

def main():
    contacts = load()
    while True:
        cmd = input('\n(a)添加 (d)删除 (s)查询 (q)退出: ').strip()
        if cmd == 'a':
            name = input('姓名: ')
            phone = input('电话: ')
            contacts.append({'name': name, 'phone': phone})
            save(contacts)
            print('已添加')
        elif cmd == 'd':
            name = input('删除谁: ')
            contacts = [c for c in contacts if c['name'] != name]
            save(contacts)
            print('已删除')
        elif cmd == 's':
            keyword = input('搜索: ')
            for c in contacts:
                if keyword in c['name'] or keyword in c['phone']:
                    print(f"  {c['name']}: {c['phone']}")
        elif cmd == 'q':
            break

if __name__ == '__main__':
    main()
```

</details>

---

## References

- [[wiki/my-learning-path/theory/python-foundation|Python 速通]]
- [[wiki/my-learning-path/theory/index|理论补全]]
