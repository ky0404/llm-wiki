---
title: Python 列表进阶
type: source
tags: [python, data-structure, list, method]
created: 2026-05-25
updated: 2026-05-25
---

# Python 列表进阶

> 来源：[[raw/Python-100-Days/09.常用数据结构之列表-2.md]]

## 核心要点

1. **添加元素**：`append(item)`末尾添加、`insert(index, item)`指定位置插入
2. **删除元素**：`remove(item)`按值删除（只删第一个）、`pop(index)`按索引删除并返回
3. **排序方法**：`sort()`原地排序、`reverse()`原地反转、`sorted()`返回新列表
4. **查找方法**：`index(item)`返回索引、`count(item)`返回出现次数
5. **列表生成式**：`[expr for var in iterable if condition]`，简洁高效
6. **嵌套列表**：列表中的元素也是列表，二维数据用嵌套列表表示

## 关键代码

```python
# 添加和删除
fruits = ['apple']
fruits.append('banana')        # 末尾添加
fruits.insert(0, 'orange')     # 指定位置插入
fruits.remove('apple')         # 按值删除
fruits.pop(0)                  # 按索引删除并返回

# 排序
nums = [3, 1, 4, 1, 5, 9]
nums.sort()                    # 原地升序
nums.sort(reverse=True)        # 原地降序
nums.reverse()                 # 原地反转
sorted_nums = sorted(nums)     # 返回新列表

# 列表生成式
squares = [x**2 for x in range(1, 11)]
evens = [x for x in range(20) if x % 2 == 0]

# 嵌套列表
scores = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

## 避坑提醒

- `remove()`只删除第一个匹配项，不存在会抛`ValueError`
- `sort()`是原地操作，返回`None`，不要写`list = list.sort()`
- 列表生成式中`if`在后是过滤条件，`if...else`在前是条件表达式

## References

- [[wiki/sources/python-08-列表基础|Python 列表基础]]
- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
