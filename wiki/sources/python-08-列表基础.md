---
title: Python 列表基础
type: source
tags: [python, data-structure, list]
created: 2026-05-25
updated: 2026-05-25
---

# Python 列表基础

> 来源：[[raw/Python-100-Days/08.常用数据结构之列表-1.md]]

## 核心要点

1. **列表定义**：`[]`字面量语法，元素用逗号分隔，可保存多个数据
2. **列表运算**：`+`拼接、`*`重复、`in/not in`成员判断
3. **索引运算**：`list[0]`正向索引，`list[-1]`反向索引
4. **切片运算**：`list[start:end:step]`，左闭右开
5. **元素遍历**：`for item in list`或`for i in range(len(list))`
6. **列表是可变类型**：可通过索引修改元素

## 关键代码

```python
# 创建列表
items = [35, 12, 99, 68]
items2 = list(range(1, 10))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 索引和切片
print(items[0])    # 35
print(items[-1])   # 68
print(items[1:3])  # [12, 99]
print(items[::2])  # [35, 99] 步长为2

# 修改元素
items[0] = 100

# 遍历
for item in items:
    print(item)
```

## 避坑提醒

- 索引越界会引发`IndexError`
- 切片不会引发越界错误，会自动调整范围
- 列表可以包含不同类型的元素，但**不建议**

## References

- [[wiki/sources/python-09-列表进阶|Python 列表进阶]]
- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
