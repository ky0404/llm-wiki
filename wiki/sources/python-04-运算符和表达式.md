---
title: Python 运算符和表达式
type: source
tags: [python, basics, operator, expression]
created: 2026-05-25
updated: 2026-05-25
---

# Python 运算符和表达式

> 来源：[[raw/Python-100-Days/04.Python语言中的运算符.md]]

## 核心要点

1. **运算符优先级**：`**` > `* / % //` > `+ -` > `比较运算` > `逻辑运算` > `赋值运算`
2. **算术运算符**：`+ - * / % //(整除) **(幂)`
3. **比较运算符**：`== != < > <= >=`，产生布尔值
4. **逻辑运算符**：`and or not`，支持短路求值
5. **赋值运算符**：`= += -= *= /=`，Python 3.8新增海象运算符`:=`
6. **成员运算符**：`in not in`，判断元素是否在序列中
7. **身份运算符**：`is is not`，判断两个变量是否引用同一对象
8. **格式化输出**：`f'{var:.2f}'`或`'%.2f' % var`

## 运算符优先级表（高→低）

| 运算符 | 描述 |
|--------|------|
| `[]` `[:]` | 索引、切片 |
| `**` | 幂 |
| `*` `/` `%` `//` | 乘、除、模、整除 |
| `+` `-` | 加、减 |
| `<=` `<` `>` `>=` | 比较运算 |
| `==` `!=` | 等于、不等于 |
| `not` `or` `and` | 逻辑运算 |

## 关键代码

```python
# 逻辑运算短路
True or print('不会执行')   # True
False and print('不会执行') # False

# 海象运算符(Python 3.8+)
if (n := len('hello')) > 3:
    print(f'长度{n}')  # 长度5

# 格式化输出
print(f'{3.14159:.2f}')  # 3.14
```

## References

- [[wiki/sources/python-03-变量和数据类型|Python 变量和数据类型]]
- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
