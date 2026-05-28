---
title: Python 面向对象应用
type: source
tags: [python, oop, enum, practice]
created: 2026-05-25
updated: 2026-05-25
---

# Python 面向对象应用

> 来源：[[raw/Python-100-Days/20.面向对象编程应用.md]]

## 核心要点

1. **枚举类Enum**：`class Suit(Enum):`定义有限集合，值不可变且有名称
2. **枚举用法**：`Suit.SPADE`、`Suit.SPADE.value`、`Suit['SPADE']`
3. **扑克游戏OOP设计**：Card类、Poker类（洗牌/发牌）、Player类，体现封装和职责分离
4. **工资结算多态实战**：不同员工类型（月薪/时薪/提成）统一接口`get_salary()`，运行时多态分发
5. **OOP设计原则**：单一职责、开闭原则、依赖抽象而非具体实现

## 关键代码

```python
from enum import Enum

class Suit(Enum):
    SPADE = '♠'
    HEART = '♥'
    CLUB = '♣'
    DIAMOND = '♦'

# 多态实战：工资结算
class Employee:
    def __init__(self, name):
        self.name = name

    def get_salary(self):
        pass  # 由子类实现

class Manager(Employee):
    def get_salary(self):
        return 15000.0

class Programmer(Employee):
    def __init__(self, name, hours=0):
        super().__init__(name)
        self.hours = hours

    def get_salary(self):
        return 200 * self.hours

# 统一接口调用 - 多态
emps = [Manager('Alice'), Programmer('Bob', 160)]
for emp in emps:
    print(f'{emp.name}: {emp.get_salary()}')
```

## 避坑提醒

- 枚举值不可修改，类型安全优于常量定义
- 多态的关键是**统一接口+子类各自实现**，不依赖具体类型判断
- `isinstance(obj, ClassName)`检查类型，但多态下应尽量用鸭子类型避免

## References

- [[wiki/sources/python-18-面向对象入门|Python 面向对象入门]]
- [[wiki/sources/python-19-面向对象进阶|Python 面向对象进阶]]
- [[wiki/concepts/python-面向对象|Python 面向对象概念]]
- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
