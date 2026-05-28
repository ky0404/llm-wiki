---
title: Python 字符串
type: source
tags: [python, data-structure, string]
created: 2026-05-25
updated: 2026-05-25
---

# Python 字符串

> 来源：[[raw/Python-100-Days/11.常用数据结构之字符串.md]]

## 核心要点

1. **字符串是不可变类型**：不能通过索引修改字符，操作均返回新字符串
2. **转义字符**：`\n`换行、`\t`制表、`\'`单引号、`\\`反斜杠
3. **原始字符串**：`r'...'`前缀，不转义，用于正则表达式和路径
4. **常用方法**：`upper()/lower()/strip()/find()/index()/count()/replace()/split()/join()`
5. **切片**：与列表切片语法相同，`s[start:end:step]`
6. **格式化输出**：f-string(Python 3.6+推荐)、`format()`方法、`%`旧式

## 关键代码

```python
# 原始字符串
path = r'C:\new\test'  # 不会转义\n和\t

# 常用方法
s = 'Hello, World!'
s.upper()          # 'HELLO, WORLD!'
s.lower()          # 'hello, world!'
s.find('World')    # 7
s.replace('World', 'Python')  # 'Hello, Python!'
s.split(', ')      # ['Hello', 'World!']
', '.join(['a','b'])  # 'a, b'

# 格式化
name, age = 'Alice', 20
print(f'{name} is {age}')           # f-string
print('{} is {}'.format(name, age))  # format方法

# 映射格式化
data = {'name': 'Bob', 'score': 95}
print('{name}: {score}'.format_map(data))
```

## 避坑提醒

- `find()`找不到返回-1，`index()`找不到抛`ValueError`
- `replace()`不修改原字符串，返回新字符串
- f-string是最推荐的格式化方式，简洁高效

## References

- [[wiki/sources/python-03-变量和数据类型|Python 变量和数据类型]]
- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
