---
title: Python 循环结构
type: source
tags: [python, basics, loop, for, while]
created: 2026-05-25
updated: 2026-05-25
---

# Python 循环结构

> 来源：[[raw/Python-100-Days/06.循环结构.md]]

## 核心要点

1. **for-in循环**：明确知道循环次数时使用，配合`range()`函数
2. **while循环**：不确定循环次数时使用，通过条件控制
3. **range()函数**：`range(stop)`、`range(start, stop)`、`range(start, stop, step)`
4. **break**：终止循环
5. **continue**：跳过本次循环，进入下一轮
6. **嵌套循环**：循环中再构造循环，如打印乘法口诀表
7. **循环变量命名惯例**：不需要使用时命名为`_`

## 关键代码

```python
# for-in循环
for i in range(1, 101):  # 1到100
    total += i

# while循环
while i <= 100:
    total += i
    i += 1

# break和continue
for i in range(1, 101):
    if i % 2 != 0:
        continue  # 跳过奇数
    total += i

# 嵌套循环：乘法口诀表
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f'{i}×{j}={i*j}', end='\t')
    print()
```

## 避坑提醒

- `while True`是死循环，必须用`break`终止
- 循环变量`i`的作用域延伸到循环外
- 嵌套循环的`break`只终止最内层循环

## References

- [[wiki/sources/python-05-分支结构|Python 分支结构]]
- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
