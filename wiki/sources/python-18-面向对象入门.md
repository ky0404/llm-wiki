---
title: Python 面向对象入门
type: source
tags: [python, oop, class, object]
created: 2026-05-25
updated: 2026-05-25
---

# Python 面向对象入门

> 来源：[[raw/Python-100-Days/18.面向对象编程入门.md]]

## 核心要点

1. **面向对象三大特征**：封装、继承、多态
2. **类与对象**：类是蓝图，对象是实例；`class ClassName:`定义类
3. **初始化方法**：`__init__(self, ...)`构造对象时自动调用
4. **self**：指向当前对象本身，类似于其他语言的`this`
5. **封装**：将数据和方法绑定在一起，隐藏内部实现，对外暴露接口
6. **继承**：子类复用父类的属性和方法，`class Child(Parent):`
7. **多态**：同一方法在不同对象上有不同表现，子类可重写父类方法
8. **object是根类**：所有类最终都继承自`object`

## 关键代码

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def study(self, course):
        print(f'{self.name}正在学习{course}')

    def __str__(self):
        return f'{self.name}({self.age})'

# 继承
class CollegeStudent(Student):
    def __init__(self, name, age, major):
        super().__init__(name, age)
        self.major = major

    # 重写父类方法 - 多态
    def study(self, course):
        print(f'{self.name}({self.major})正在学习{course}')

# 使用
stu = CollegeStudent('Alice', 20, 'CS')
stu.study('Python')  # Alice(CS)正在学习Python
print(stu)           # Alice(20)
```

## 避坑提醒

- `__init__`不是构造函数，是初始化方法；`__new__`才是构造方法
- `self`必须显式写出，不像其他语言的`this`可省略
- 继承时务必调用`super().__init__()`初始化父类部分

## References

- [[wiki/sources/python-19-面向对象进阶|Python 面向对象进阶]]
- [[wiki/concepts/python-面向对象|Python 面向对象概念]]
- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
