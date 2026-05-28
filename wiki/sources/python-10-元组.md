---
title: Python 元组
type: source
tags: [python, data-structure, tuple]
created: 2026-05-25
updated: 2026-05-25
---

# Python 元组

> 来源：[[raw/Python-100-Days/10.常用数据结构之元组.md]]

## 核心要点

1. **元组是不可变类型**：创建后不能修改、添加、删除元素
2. **创建语法**：`()`字面量或`tuple()`构造，单元素元组必须加逗号`(1,)`
3. **打包和解包**：多个值赋给一个变量是打包，一个变量赋给多个值是解包
4. **交换变量**：`a, b = b, a`利用解包实现，无需临时变量
5. **元组 vs 列表**：元组不可变更安全、可作为字典键、性能略优

## 关键代码

```python
# 创建元组
t = (1, 2, 3)
single = (1,)    # 单元素元组，逗号不能省
empty = ()

# 解包
x, y, z = t
a, b, *rest = (1, 2, 3, 4, 5)  # a=1, b=2, rest=[3,4,5]

# 交换变量
a, b = b, a

# 元组不可变
# t[0] = 10  # TypeError! 不能修改
```

## 避坑提醒

- 单元素元组`(1,)`的逗号不能省，`(1)`只是整数1
- 元组不可变指的是**顶层引用不可变**，若元素是可变对象（如列表），其内容仍可修改
- 函数返回多个值本质上就是返回元组

## References

- [[wiki/sources/python-08-列表基础|Python 列表基础]]
- [[wiki/sources/python-09-列表进阶|Python 列表进阶]]
- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
