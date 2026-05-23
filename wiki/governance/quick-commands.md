---
title: 保护策略快速命令手册
type: synthesis
tags: [governance, commands, quick-reference]
sources: [scripts/path_guard.py, scripts/write_wrapper.py]
created: 2026-05-01
updated: 2026-05-01
---

# 保护策略快速命令手册

> 本手册收录所有常用命令，方便快速查阅

---

## 一、路径检查

### 检查单个路径是否受保护

```bash
python scripts/path_guard.py check "AGENTS.md"
python scripts/path_guard.py check "skills/wiki-maintainer.md"
```

输出示例：
```
AGENTS.md: 🔴 受保护
skills/wiki-maintainer.md: 🔴 受保护
wiki/sources/test.md: 🟢 可写入
```

---

## 二、授权管理

### 2.1 获取授权

```bash
python scripts/path_guard.py authorize "AGENTS.md" "修改原因说明"
```

输出示例：
```
✅ 授权成功
   授权版本号: guard-20260501-abc123
   使用方式: safe_write('AGENTS.md', content, authorized=True, auth_version='guard-20260501-abc123')
```

### 2.2 撤销授权

```bash
python scripts/path_guard.py revoke "guard-20260501-abc123"
```

输出示例：
```
✅ 撤销成功: guard-20260501-abc123
```

### 2.3 列出所有有效授权

```bash
python scripts/path_guard.py list
```

### 2.4 显示保护状态

```bash
python scripts/path_guard.py status
```

输出示例：
```
==================================================
保护状态
==================================================
受保护路径数: 4
有效授权数: 2
环境变量覆盖: False
全局锁: 已启用
```

---

## 三、测试与验证

### 3.1 运行完整测试套件

```bash
python scripts/guard_tests.py
```

预期输出：
```
==================================================
总计: 19 通过, 0 失败
==================================================
```

### 3.2 运行路径保护测试

```bash
python scripts/path_guard.py
```

---

## 四、Python 编程接口

### 4.1 导入方式

```python
# 方式1：直接使用 path_guard
from scripts.path_guard import (
    is_protected_path,
    safe_write,
    safe_write_with_lock,
    authorize_write,
    revoke_authorization,
    is_authorized
)

# 方式2：使用统一写入封装（推荐）
from scripts.write_wrapper import (
    write_file,
    write_file_with_lock,
    write_text,
    check_and_warn
)
```

### 4.2 常用代码示例

```python
# 检查路径是否受保护
if is_protected_path("AGENTS.md"):
    print("需要授权才能写入")

# 获取授权
auth_version = authorize_write("AGENTS.md", "更新规则")
print(f"授权版本号: {auth_version}")

# 使用授权写入（方式1）
safe_write("AGENTS.md", new_content, authorized=True, auth_version=auth_version)

# 使用授权写入（方式2）
write_file("AGENTS.md", new_content, authorized=True, auth_version=auth_version)

# 普通写入（非保护路径）
write_text("my-learning-path/test.md", "内容")

# 带锁的安全写入（防止并发）
write_file_with_lock("AGENTS.md", new_content, authorized=True)

# 检查并警告
check_and_warn("skills/wiki-maintainer.md")
```

---

## 五、环境变量

### 5.1 临时绕过保护（紧急情况使用）

```bash
ALLOW_GUARD_OVERRIDE=true python scripts/path_guard.py authorize "AGENTS.md" "紧急修改"
```

---

## 六、快速检查清单

| 操作 | 命令 |
|------|------|
| 检查路径 | `python scripts/path_guard.py check "<路径>"` |
| 获取授权 | `python scripts/path_guard.py authorize "<路径>" "<原因>"` |
| 撤销授权 | `python scripts/path_guard.py revoke "<授权版本号>"` |
| 列出授权 | `python scripts/path_guard.py list` |
| 显示状态 | `python scripts/path_guard.py status` |
| 运行测试 | `python scripts/guard_tests.py` |

---

## 七、受保护路径清单

| 路径 | 说明 |
|------|------|
| `AGENTS.md` | 最高规则文档 |
| `skills/` | 技能模块目录 |
| `wiki/skills/` | Wiki 技能目录 |
| `wiki/synthesis/knowledge-base-evolution-*.md` | 演化规则文档 |

---

## 八、常见问题

### Q1: 写入被拦截怎么办？
```
1. 确认是否需要修改受保护路径
2. 如果需要：提交 [进化提议] 获取审批
3. 审批通过后：使用 authorize_write 获取授权版本号
4. 使用授权版本号调用 safe_write
```

### Q2: 如何回滚？
```
1. 备份文件位置：.gc_backups/
2. 撤销授权：python scripts/path_guard.py revoke "<授权版本号>"
3. 手动恢复备份文件
```

### Q3: 并发写入冲突？
```
使用带锁版本：write_file_with_lock() 或 safe_write_with_lock()
```

---

## References

- [[wiki/governance/guard-manual.md|完整使用手册]]
- [[wiki/governance/demonstration.md|演示摘要]]
- [[scripts/path_guard.py|路径保护工具源码]]