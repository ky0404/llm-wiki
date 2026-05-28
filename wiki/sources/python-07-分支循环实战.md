---
title: Python 分支循环实战
type: source
tags: [python, practice, algorithm]
created: 2026-05-25
updated: 2026-05-25
---

# Python 分支循环实战

> 来源：[[raw/Python-100-Days/07.分支和循环结构实战.md]]

## 核心要点

1. **穷举法/暴力搜索**：列举所有可能候选项，检查是否符合条件
2. **素数判断优化**：只需检查到`√n`即可
3. **斐波那契数列**：`a, b = b, a + b`递推公式
4. **水仙花数**：三位数各位数字立方和等于自身，如`153 = 1³+5³+3³`
5. **数字拆分技巧**：`个位=n%10`，`十位=n//10%10`，`百位=n//100`

## 经典算法

### 素数判断

```python
for num in range(2, 100):
    is_prime = True
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            is_prime = False
            break
    if is_prime:
        print(num)
```

### 斐波那契数列

```python
a, b = 0, 1
for _ in range(20):
    a, b = b, a + b
    print(a)
```

### 水仙花数

```python
for num in range(100, 1000):
    low = num % 10
    mid = num // 10 % 10
    high = num // 100
    if num == low**3 + mid**3 + high**3:
        print(num)  # 153, 370, 371, 407
```

### 百钱百鸡（穷举法）

```python
for x in range(0, 21):        # 公鸡最多20只
    for y in range(0, 34):    # 母鸡最多33只
        z = 100 - x - y       # 小鸡
        if z % 3 == 0 and 5*x + 3*y + z//3 == 100:
            print(f'公鸡{x}只, 母鸡{y}只, 小鸡{z}只')
```

## References

- [[wiki/sources/python-05-分支结构|Python 分支结构]]
- [[wiki/sources/python-06-循环结构|Python 循环结构]]
- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
