---
title: 保护策略演示摘要
type: synthesis
tags: [governance, demo, interview, security]
sources: [scripts/path_guard.py, wiki/governance/guard-manual.md]
created: 2026-05-01
updated: 2026-05-01
---

# 保护策略演示摘要

## 一、设计理念

**核心目标**：保证治理性文件（AGENTS.md、skills等）的改动必须经过授权、可追溯、可回滚。

**三层保护**：
1. **路径保护** - 写入前拦截，默认拒绝治理性文件
2. **授权治理** - 授权版本号 + 演化提议流程
3. **审计回滚** - 日志完整记录 + 写入前备份

## 二、演示案例

### 案例1：未授权写入被拦截

```bash
$ python scripts/path_guard.py authorize "AGENTS.md" "测试"
错误：AGENTS.md 是受保护路径，需要授权才能写入
```

**日志记录**：
```
2026-05-01 保护操作
操作对象：AGENTS.md
触发原因：尝试写入受保护路径，未获得授权
拦截结果：已拦截
授权状态：待审
下一步计划：提交演化提议等待审批
```

### 案例2：授权通过后写入

```bash
# 1. 获取授权
$ python scripts/path_guard.py authorize "AGENTS.md" "更新规则"
✅ 授权成功
   授权版本号: guard-20260501-abc123

# 2. 使用授权写入
$ python -c "
from scripts.path_guard import safe_write
safe_write('AGENTS.md', '# 新内容', authorized=True, auth_version='guard-20260501-abc123')
"
✅ 写入成功
```

**日志记录**：
```
2026-05-01 保护操作
操作对象：AGENTS.md
触发原因：授权版本号: guard-20260501-abc123, 原因: 更新规则
拦截结果：已放行
授权状态：已通过
授权版本号：guard-20260501-abc123
下一步计划：执行修改
```

### 案例3：授权撤销后再次拦截

```bash
$ python scripts/path_guard.py revoke "guard-20260501-abc123"
✅ 撤销成功

$ python scripts/path_guard.py authorize "AGENTS.md" "再次修改"
错误：AGENTS.md 是受保护路径，需要授权才能写入
```

## 三、技术实现

| 组件 | 功能 |
|------|------|
| `path_guard.py` | 6个核心API：is_protected_path, safe_write, authorize_write, revoke_authorization, backup_file, log_protection |
| `write_wrapper.py` | 统一写入封装，4个函数 |
| `guard_tests.py` | 19个测试用例，全部通过 |
| `.guard_authorizations.json` | 授权版本号持久化 |
| `guard-check.yml` | CI/CD自动检查 |

## 四、面试亮点

1. **设计思想**：三层保护，从被动防御到主动治理
2. **工程实现**：文件锁防止并发、写入前备份支持回滚
3. **可追溯**：所有操作记录到log.md，完整审计链
4. **自动化**：CI/CD集成保护检查，PR/合并强制通过

## 五、核心数字

- 受保护路径：4个（AGENTS.md, skills/, wiki/skills/, synthesis/knowledge-base-evolution-*.md）
- 授权版本号格式：guard-YYYYMMDD-8位随机
- 测试覆盖率：19个用例，100%通过
- 自动备份：.gc_backups/目录
- 日志记录：35条保护操作日志

---

## References

- `scripts/path_guard.py`
- [[wiki/governance/guard-manual.md|完整使用手册]]
- [[log|操作日志]]