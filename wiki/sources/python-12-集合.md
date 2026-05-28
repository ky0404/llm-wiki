---
title: Python 集合
type: source
tags: [python, data-structure, set]
created: 2026-05-25
updated: 2026-05-25
---

# Python 集合

> 来源：[[raw/Python-100-Days/12.常用数据结构之集合.md]]

## 核心要点

1. **集合是可变、无序、不重复的容器**：自动去重
2. **数学运算**：交集`&`、并集`|`、差集`-`、对称差集`^`
3. **方法运算**：`intersection()/union()/difference()/symmetric_difference()`
4. **元素必须是hashable类型**：不可变类型（数字、字符串、元组）可作元素，列表和字典不行
5. **集合生成式**：`{expr for var in iterable if condition}`
6. **不可变集合**：`frozenset`，可作为集合的元素或字典的键
7. **常用场景**：去重、成员判断（O(1)复杂度）、数学集合运算

## 关键代码

```python
# 创建集合
s = {1, 2, 3}
s2 = set([1, 2, 2, 3])  # {1, 2, 3} 自动去重

# 数学运算
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
a & b   # {3, 4}      交集
a | b   # {1,2,3,4,5,6} 并集
a - b   # {1, 2}      差集
a ^ b   # {1, 2, 5, 6} 对称差集

# 去重
names = ['Alice', 'Bob', 'Alice', 'Charlie']
unique = list(set(names))

# 集合生成式
squares = {x**2 for x in range(10)}
```

## 避坑提醒

- 空集合用`set()`创建，`{}`创建的是空字典
- 集合无序，不能用索引访问
- 成员判断用集合比列表快得多（哈希表O(1) vs 列表O(n)）

## References

- [[wiki/sources/python-13-字典|Python 字典]]
- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
