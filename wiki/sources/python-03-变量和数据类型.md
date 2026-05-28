---
title: Python 变量和数据类型
type: source
tags: [python, basics, variable, datatype]
created: 2026-05-25
updated: 2026-05-25
---

# Python 变量和数据类型

> 来源：[[raw/Python-100-Days/03.Python语言中的变量.md]]

## 核心要点

1. **变量是数据的载体**：一块用来保存数据的内存空间，值可被读取和修改
2. **四种基本数据类型**：`int`(整型)、`float`(浮点型)、`str`(字符串型)、`bool`(布尔型)
3. **整数支持多进制**：二进制`0b100`、八进制`0o100`、十六进制`0x100`
4. **变量命名规则**：字母/数字/下划线构成，数字不能开头，大小写敏感，避开关键字
5. **命名惯例**：小写字母+下划线连接，受保护变量`_name`，私有变量`__name`
6. **类型转换函数**：`int()`、`float()`、`str()`、`chr()`、`ord()`
7. **类型检查**：使用`type()`函数检查变量类型

## 关键代码

```python
a = 45        # int
b = 123.45    # float
c = 'hello'   # str
d = True      # bool

print(type(a))  # <class 'int'>
print(int('123'))       # 字符串转整数
print(int('100', base=2))  # 二进制字符串转整数
```

## 避坑提醒

- 变量命名必须**见名知意**，避免`a`、`b`、`c`这种无意义命名
- `str`转`bool`时，非空字符串都是`True`
- `bool`转`int`时，`True`→1，`False`→0

## References

- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
