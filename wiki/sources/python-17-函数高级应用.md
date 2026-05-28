---
title: Python 函数高级应用
type: source
tags: [python, function, decorator, recursion]
created: 2026-05-25
updated: 2026-05-25
---

# Python 函数高级应用

> 来源：[[raw/Python-100-Days/17.函数高级应用.md]]

## 核心要点

1. **带参数装饰器**：三层嵌套，最外层接收装饰器参数，如`@repeat(3)`
2. **装饰器执行顺序**：多个装饰器从下往上执行等效包装，从上往下执行等效调用
3. **递归经典案例**：阶乘、斐波那契、汉诺塔，关键在于找递推关系和边界条件
4. **递归优化**：记忆化（缓存已计算结果）避免重复计算
5. **高阶函数组合**：`map`+`filter`+`reduce`实现函数式数据处理

## 关键代码

```python
# 带参数装饰器
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello(name):
    print(f'Hello, {name}!')

# 汉诺塔递归
def hanoi(n, source, target, auxiliary):
    if n == 1:
        print(f'{source} → {target}')
    else:
        hanoi(n-1, source, auxiliary, target)
        print(f'{source} → {target}')
        hanoi(n-1, auxiliary, target, source)

# 记忆化递归优化
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

# reduce
from functools import reduce
reduce(lambda x, y: x + y, [1, 2, 3, 4, 5])  # 15
```

## 避坑提醒

- 带参数装饰器是三层函数，容易写错层级
- 汉诺塔时间复杂度O(2ⁿ)，层数大时不可用
- `lru_cache`只能缓存hashable参数的调用结果

## References

- [[wiki/sources/python-16-函数进阶|Python 函数进阶]]
- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
