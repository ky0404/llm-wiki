---
title: 保护策略使用手册
type: synthesis
tags: [governance, protection, security, guide]
sources: [scripts/path_guard.py]
created: 2026-05-01
updated: 2026-05-01
---

# 保护策略使用手册

## 一、概述

本手册描述如何使用路径保护工具 (`scripts/path_guard.py`) 来管理对治理性文件的修改。

**核心原则**：
- 默认拒绝写入治理性文件
- 只有获得正式授权后才允许修改
- 所有操作都有完整的审计日志

## 二、受保护路径

| 路径 | 说明 |
|------|------|
| `AGENTS.md` | 最高规则文档 |
| `skills/` | 技能模块目录 |
| `wiki/skills/` | Wiki 技能目录 |
| `wiki/synthesis/knowledge-base-evolution-*.md` | 演化规则文档 |

## 三、授权工作流

### 3.1 获取授权

```bash
# 使用 CLI 获取授权
python scripts/path_guard.py authorize "AGENTS.md" "修改原因说明"
```

成功后会返回授权版本号：
```
✅ 授权成功
   授权版本号: guard-20260501-12b3bfa0
   使用方式: safe_write('AGENTS.md', content, authorized=True, auth_version='guard-20260501-12b3bfa0')
```

### 3.2 使用授权写入

```python
from scripts.path_guard import safe_write, is_authorized

# 方式1：直接授权
safe_write("AGENTS.md", new_content, authorized=True)

# 方式2：使用授权版本号
auth_version = "guard-20260501-12b3bfa0"
if is_authorized(auth_version, "AGENTS.md"):
    safe_write("AGENTS.md", content, authorized=True, auth_version=auth_version)
```

### 3.3 撤销授权

```bash
python scripts/path_guard.py revoke "guard-20260501-12b3bfa0"
```

### 3.4 检查路径状态

```bash
# 检查路径是否受保护
python scripts/path_guard.py check "skills/wiki-maintainer.md"

# 列出所有有效授权
python scripts/path_guard.py list

# 显示保护状态
python scripts/path_guard.py status
```

## 四、演化提议模板

对治理性文件的任何修改必须先提交 [进化提议]：

```markdown
[进化提议] 新增 / 优化规则：【规则标题】
适用场景：【适用场景描述】
规则内容：
- 规则1
- 规则2

执行依据：【为什么需要修改，解决了什么问题】

审批状态：【待审/已通过/已拒绝】
```

## 五、常见问题

### 5.1 写入被拦截

**问题**：尝试修改 AGENTS.md 时被拦截

**解决**：
1. 提交 [进化提议]
2. 获得批准后获取授权版本号
3. 使用授权版本号写入

### 5.2 紧急情况

**问题**：需要紧急修改但来不及走审批流程

**解决**：设置环境变量临时绕过（仅紧急使用）
```bash
ALLOW_GUARD_OVERRIDE=true python scripts/path_guard.py ...
```

### 5.3 并发写入冲突

**问题**：多个进程同时写入被保护文件

**解决**：使用带锁的安全写入
```python
from scripts.path_guard import safe_write_with_lock
safe_write_with_lock("AGENTS.md", content, authorized=True)
```

## 六、审计日志

所有保护相关操作都会记录到 `log.md`：

```
2026-05-01 保护操作
操作对象：AGENTS.md
触发原因：授权版本号: guard-20260501-xxx, 原因: 测试
拦截结果：已放行
授权状态：已通过
授权版本号：guard-20260501-xxx
下一步计划：执行修改
```

## 七、日常普通修改流程（不涉及治理性文件）

### 步骤0：事前检查
确认要改动的不是治理性文件（AGENTS.md、skills/、wiki/skills/、synthesis/knowledge-base-evolution-*.md）

### 步骤1：dry-run 验证
```bash
# 使用 write_wrapper 进行干运行检查
python3 -c "
from scripts.write_wrapper import check_and_warn
paths = ['my-learning-path/test.md', 'concepts/test.md']
for p in paths:
    check_and_warn(p)
"
```

### 步骤2：进行改动
使用统一写入封装：
```python
from scripts.write_wrapper import write_text

# 写入非保护路径
write_text("my-learning-path/new-file.md", "# 新内容")
```

### 步骤3：日志记录
在 log.md 中记录改动要点

### 步骤4：审计与回顾
定期检查 log.md 中的改动记录

---

## 八、治理性修改正式流程（必须）

### 触发条件
需要修改 AGENTS.md、skills/、wiki/skills/、synthesis/knowledge-base-evolution-*.md 时

### 流程步骤

1. **提交进化提议**
   在 log.md 中写入：
   ```markdown
   [进化提议] 新增 / 优化规则：【规则标题】
   适用场景：【适用场景描述】
   规则内容：
   - 规则1
   - 规则2
   执行依据：【为什么需要修改】
   审批状态：【待审】
   ```

2. **获得审批**
   审批通过后获取授权版本号：
   ```bash
   python scripts/path_guard.py authorize "AGENTS.md" "修改原因"
   ```

3. **执行写入**
   ```python
   from scripts.path_guard import safe_write
   
   auth_version = "guard-20260501-xxxxxx"
   safe_write("AGENTS.md", new_content, authorized=True, auth_version=auth_version)
   ```

4. **记录日志**
   自动记录到 log.md

5. **如需撤销**
   ```bash
   python scripts/path_guard.py revoke "guard-20260501-xxxxxx"
   ```

---

## 九、审计日志格式

所有保护相关操作记录到 log.md：

```
2026-05-01 保护操作
操作对象：AGENTS.md
触发原因：授权版本号: guard-20260501-xxx, 原因: 更新规则
拦截结果：已放行
授权状态：已通过
授权版本号：guard-20260501-xxx
下一步计划：执行修改
```

---

## 十、快速检查清单

| 检查项 | 命令 |
|--------|------|
| 检查路径是否受保护 | `python scripts/path_guard.py check <path>` |
| 获取授权 | `python scripts/path_guard.py authorize <path> <原因>` |
| 撤销授权 | `python scripts/path_guard.py revoke <auth_version>` |
| 列出授权 | `python scripts/path_guard.py list` |
| 显示状态 | `python scripts/path_guard.py status` |
| 运行测试 | `python scripts/guard_tests.py` |

---

## References

- [[scripts/path_guard.py|路径保护工具源码]]
- [[scripts/guard_tests.py|测试套件]]
- [[AGENTS.md|最高规则文档]]
- [[log|操作日志]]