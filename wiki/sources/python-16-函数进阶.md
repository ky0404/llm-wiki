---
title: Python 函数进阶
type: source
tags: [python, function, higher-order, lambda]
created: 2026-05-25
updated: 2026-05-25
---

# Python 函数进阶

> 来源：[[raw/Python-100-Days/16.函数使用进阶.md]]

## 核心要点

1. **高阶函数**：函数可以作为参数传递或作为返回值
2. **Lambda表达式**：`lambda params: expr`，匿名函数，单行表达式
3. **常用高阶函数**：`map(func, iterable)`、`filter(func, iterable)`、`sorted(iterable, key=func)`
4. **偏函数**：`functools.partial(func, **kwargs)`固定部分参数生成新函数
5. **装饰器基础**：`@decorator`语法糖，在不修改函数代码的前提下增强功能
6. **递归函数**：函数调用自身，必须有递归出口（边界条件）

## 关键代码

```python
# Lambda
square = lambda x: x ** 2
add = lambda a, b: a + b

# map和filter
list(map(lambda x: x**2, range(1, 6)))      # [1,4,9,16,25]
list(filter(lambda x: x%2==0, range(10)))   # [0,2,4,6,8]

# sorted with key
students = [('Alice', 95), ('Bob', 80), ('Charlie', 90)]
sorted(students, key=lambda x: x[1], reverse=True)

# 装饰器
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f'{func.__name__}耗时: {time.time()-start:.4f}s')
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)

# 递归
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

## 避坑提醒

- Lambda只能写单个表达式，不能包含语句（如if语句块）
- 递归深度有上限（默认1000），深递归要用循环替代
- 装饰器会改变原函数的`__name__`等元信息，可用`@functools.wraps`保留

## References

- [[wiki/sources/python-14-函数和模块|Python 函数和模块]]
- [[wiki/sources/python-17-函数高级应用|Python 函数高级应用]]
- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
