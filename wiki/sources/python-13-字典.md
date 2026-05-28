---
title: Python 字典
type: source
tags: [python, data-structure, dict]
created: 2026-05-25
updated: 2026-05-25
---

# Python 字典

> 来源：[[raw/Python-100-Days/13.常用数据结构之字典.md]]

## 核心要点

1. **键值对容器**：`{key: value}`语法，通过键快速查找值（O(1)复杂度）
2. **键必须不可变**：字符串、数字、元组可作键，列表和字典不行
3. **常用方法**：`get()/keys()/values()/items()/pop()/update()`
4. **字典生成式**：`{key_expr: val_expr for var in iterable if condition}`
5. **JSON转换**：`json.dumps(dict)`→JSON字符串，`json.loads(json_str)`→字典
6. **遍历方式**：`.items()`同时获取键和值

## 关键代码

```python
# 创建字典
person = {'name': 'Alice', 'age': 20}

# 访问和修改
person['name']              # 'Alice'
person.get('score', 0)      # 不存在返回0，不报错
person['score'] = 95        # 添加或修改

# 常用方法
person.keys()               # 所有键
person.values()             # 所有值
person.items()              # 所有键值对
person.pop('age')           # 删除并返回
person.update({'score': 100})  # 批量更新

# 遍历
for key, value in person.items():
    print(f'{key}: {value}')

# 字典生成式
squares = {x: x**2 for x in range(1, 6)}  # {1:1, 2:4, 3:9, 4:16, 5:25}

# JSON转换
import json
json_str = json.dumps(person, ensure_ascii=False)
```

## 避坑提醒

- 直接`dict[key]`访问不存在的键会抛`KeyError`，优先用`get(key, default)`
- 字典从Python 3.7起保证插入顺序
- `json.dumps()`中文需加`ensure_ascii=False`

## References

- [[wiki/sources/python-12-集合|Python 集合]]
- [[wiki/my-learning-path/theory/python-foundation|Python 速通体系]]
