---
title: Python 分支结构
type: source
tags: [python, basics, branch, if]
created: 2026-05-25
updated: 2026-05-25
---

# Python 分支结构

> 来源：[[raw/Python-100-Days/05.分支结构.md]]

## 核心要点

1. **if-elif-else结构**：根据条件选择执行路径
2. **代码块通过缩进表示**：通常使用4个空格，**禁止使用Tab**
3. **Python特色**：支持链式比较`18.5 <= bmi < 24`
4. **match-case语法**：Python 3.10新增的模式匹配
5. **嵌套分支**：可以在if/elif/else中再构造分支，但**扁平化优于嵌套**

## 关键代码

```python
# if-elif-else
if bmi < 18.5:
    print('体重过轻')
elif bmi < 24:
    print('身材很棒')
else:
    print('体重过重')

# match-case (Python 3.10+)
match status_code:
    case 400 | 405: description = 'Invalid Request'
    case 401 | 403 | 404: description = 'Not Allowed'
    case _: description = 'Unknown'
```

## 避坑提醒

- `if`语句末尾必须有冒号`:`
- 所有特殊字符必须在**英文输入法**下输入
- **扁平化优于嵌套**：避免过多层次的嵌套分支

## References

- [[wiki/sources/python-04-运算符和表达式|Python 运算符和表达式]]
- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
