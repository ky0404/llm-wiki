---
title: Python 函数实战
type: source
tags: [python, function, practice]
created: 2026-05-25
updated: 2026-05-25
---

# Python 函数实战

> 来源：[[raw/Python-100-Days/15.函数应用实战.md]]

## 核心要点

1. **随机验证码**：`random.choices(population, k=n)`从序列中随机选n个
2. **最大公约数GCD**：辗转相除法（欧几里得算法），`gcd(a,b) = gcd(b, a%b)`
3. **最小公倍数LCM**：`lcm(a,b) = a*b // gcd(a,b)`
4. **CRAPS赌博游戏**：综合运用分支和循环的实战案例
5. **函数设计原则**：单一职责、参数合理默认值、返回值而非直接打印

## 关键代码

```python
import random

# 随机验证码
def generate_code(code_len=4):
    all_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.choices(all_chars, k=code_len))

# GCD - 辗转相除法
def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

# LCM
def lcm(x, y):
    return x * y // gcd(x, y)

# 判断素数
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
```

## 避坑提醒

- `random.choices()`是可重复采样，`random.sample()`是不重复采样
- 辗转相除法比暴力枚举效率高得多
- 函数应该返回结果，而非直接`print`，便于复用

## References

- [[wiki/sources/python-14-函数和模块|Python 函数和模块]]
- [[wiki/sources/python-07-分支循环实战|Python 分支循环实战]]
- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
