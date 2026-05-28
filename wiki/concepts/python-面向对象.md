---
title: Python 面向对象
type: concept
tags: [python, oop, paradigm]
created: 2026-05-25
updated: 2026-05-25
---

# Python 面向对象

## 定义

面向对象编程（OOP）是一种编程范式，将数据和处理数据的方法封装为**对象**，通过**类**定义对象的蓝图，支持**封装**、**继承**、**多态**三大特征。

## 三大特征

| 特征 | 含义 | 关键机制 |
|------|------|----------|
| 封装 | 隐藏内部实现，对外暴露接口 | `@property`、`__name`名称修饰 |
| 继承 | 子类复用父类的属性和方法 | `class Child(Parent)`、`super()` |
| 多态 | 同一方法在不同对象上表现不同 | 方法重写、鸭子类型 |

## 核心概念速查

- **类(Class)**：对象的模板/蓝图 → `class ClassName:`
- **对象(Object)**：类的实例 → `obj = ClassName()`
- **self**：指向当前实例，类似其他语言的`this`
- **__init__**：初始化方法，创建对象时自动调用
- **@property**：将方法变为属性，控制读写访问
- **@classmethod**：类方法，第一个参数是`cls`
- **@staticmethod**：静态方法，不需要`self`或`cls`
- **__slots__**：限制实例属性，节省内存
- **MRO**：方法解析顺序，C3线性化算法

## 与其他语言对比

| 特性 | Python | Java/C++ |
|------|--------|----------|
| 访问控制 | 约定式（`_`/`__`） | 关键字（private/protected/public） |
| 多态 | 鸭子类型 | 接口/虚函数 |
| 继承 | 多继承 | 单继承+接口 |
| self/this | 显式self | 隐式this |

## 面试高频问题

1. Python的`__name`是真正的私有吗？→ 不是，名称修饰后可通过`_ClassName__name`访问
2. `@property`的作用？→ 将方法变为属性调用，实现受控访问
3. 什么是鸭子类型？→ 不关注对象类型本身，只关注其行为（方法/属性）
4. MRO是什么？→ 方法解析顺序，Python使用C3线性化算法处理多继承

## 学习路径

1. 入门：[[wiki/sources/python-18-面向对象入门|面向对象入门]] — 类/对象/封装/继承/多态基础
2. 进阶：[[wiki/sources/python-19-面向对象进阶|面向对象进阶]] — @property/类方法/静态方法/MRO
3. 应用：[[wiki/sources/python-20-面向对象应用|面向对象应用]] — Enum枚举/扑克游戏/工资结算多态

## References

- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
