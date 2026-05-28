---
title: Python 函数和模块
type: source
tags: [python, function, module]
created: 2026-05-25
updated: 2026-05-25
---

# Python 函数和模块

> 来源：[[raw/Python-100-Days/14.函数和模块.md]]

## 核心要点

1. **函数定义**：`def func_name(params):`，用`return`返回值
2. **参数类型**：位置参数、默认参数、可变参数`*args`、关键字参数`**kwargs`
3. **命名关键字参数**：`*`后的参数必须用关键字传递，如`def f(name, *, age)`
4. **模块导入**：`import module`、`from module import name`、`as`别名
5. **作用域**：LEGB规则（Local → Enclosing → Global → Built-in）
6. **`global`关键字**：在函数内修改全局变量需声明`global`
7. **`__name__`判断**：`if __name__ == '__main__':`区分模块直接运行还是被导入

## 关键代码

```python
# 函数定义
def add(a, b=0, *args, **kwargs):
    return a + b + sum(args)

# 命名关键字参数
def register(name, *, age, gender):
    print(f'{name}, {age}, {gender}')
register('Alice', age=20, gender='F')  # age和gender必须关键字传递

# 可变参数
def calc(*numbers):
    total = 0
    for n in numbers:
        total += n
    return total

# 模块导入
import math
from random import randint as ri

# 主入口
if __name__ == '__main__':
    print('直接运行')
```

## 避坑提醒

- 默认参数不要用可变对象（如`def f(a=[]):`），默认值只在定义时创建一次
- 可变参数`*args`收集为元组，`**kwargs`收集为字典
- 避免使用`from module import *`，命名空间污染严重

## References

- [[wiki/sources/python-15-函数实战|Python 函数实战]]
- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
