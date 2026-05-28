---
title: Python 面向对象进阶
type: source
tags: [python, oop, property, inheritance, polymorphism]
created: 2026-05-25
updated: 2026-05-25
---

# Python 面向对象进阶

> 来源：[[raw/Python-100-Days/19.面向对象编程进阶.md]]

## 核心要点

1. **可见性**：`__name`名称修饰（非真正私有）、`_name`约定受保护
2. **@property**：将方法变为属性调用，用于getter/setter控制访问
3. **__slots__**：限制实例可动态添加的属性，节省内存
4. **类方法@classmethod**：第一个参数是`cls`（类本身），可通过类名调用
5. **静态方法@staticmethod**：不需要`self`或`cls`，与类相关但不需要访问实例/类数据
6. **继承与super()**：`super().__init__()`调用父类初始化，遵循MRO顺序
7. **多态**：子类重写父类方法，运行时根据对象类型决定调用哪个版本
8. **方法解析顺序MRO**：C3线性化算法，`ClassName.mro()`查看

## 关键代码

```python
class Person:
    __slots__ = ('_name', '_age')

    def __init__(self, name, age):
        self._name = name
        self._age = age

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 0 or value > 150:
            raise ValueError('无效年龄')
        self._age = value

    @classmethod
    def from_string(cls, info_str):
        name, age = info_str.split(',')
        return cls(name, int(age))

    @staticmethod
    def is_adult(age):
        return age >= 18

# 继承与多态
class Student(Person):
    def __init__(self, name, age, score):
        super().__init__(name, age)
        self._score = score

    @property
    def score(self):
        return self._score
```

## 避坑提醒

- `__name`不是真正的私有，外部可通过`_ClassName__name`访问
- `__slots__`不会被子类继承，子类需重新声明
- `@property`的setter必须与getter同名

## References

- [[wiki/sources/python-18-面向对象入门|Python 面向对象入门]]
- [[wiki/sources/python-20-面向对象应用|Python 面向对象应用]]
- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
