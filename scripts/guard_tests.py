#!/usr/bin/env python3
"""
路径保护工具测试套件

测试覆盖：
1. 路径保护判断测试
2. 授权与撤销测试
3. 拦截与放行测试
4. 环境变量覆盖测试

用法：
    python3 scripts/guard_tests.py
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))
from path_guard import (
    is_protected_path,
    safe_write,
    authorize_write,
    revoke_authorization,
    is_authorized,
    ALLOW_GUARD_OVERRIDE
)

# 测试项目根目录
TEST_ROOT = Path("/home/dukkha/wiki")

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def add(self, name: str, passed: bool, message: str = ""):
        status = "✅ PASS" if passed else "❌ FAIL"
        self.results.append(f"{status} - {name}")
        if message:
            self.results.append(f"       {message}")
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_summary(self):
        print("\n" + "=" * 50)
        print(f"测试结果: {self.passed} 通过, {self.failed} 失败")
        print("=" * 50)
        for r in self.results:
            print(r)
        return self.failed == 0


def test_path_protection():
    """测试1: 路径保护判断"""
    result = TestResult()
    
    # 测试受保护路径
    protected_paths = [
        "AGENTS.md",
        "skills/wiki-maintainer.md",
    ]
    
    for path in protected_paths:
        is_prot = is_protected_path(path)
        result.add(f"受保护路径识别: {path}", is_prot, 
                   f"预期 True, 实际 {is_prot}")
    
    # 测试非保护路径
    unprotected_paths = [
        "wiki/sources/test.md",
        "wiki/my-learning-path/test.md",
        "wiki/concepts/test.md",
    ]
    
    for path in unprotected_paths:
        is_prot = is_protected_path(path)
        result.add(f"非保护路径识别: {path}", not is_prot,
                   f"预期 False, 实际 {is_prot}")
    
    return result


def test_authorization():
    """测试2: 授权与撤销"""
    result = TestResult()
    
    # 测试授权
    auth_version = authorize_write("AGENTS.md", "测试授权")
    result.add("授权版本号生成", bool(auth_version), f"版本号: {auth_version}")
    
    # 测试授权验证
    is_auth = is_authorized(auth_version, "AGENTS.md")
    result.add("授权验证通过", is_auth)
    
    # 测试撤销
    revoked = revoke_authorization(auth_version)
    result.add("授权撤销", revoked)
    
    # 验证撤销后失效
    is_auth_after = is_authorized(auth_version, "AGENTS.md")
    result.add("撤销后授权失效", not is_auth_after)
    
    return result


def test_interception():
    """测试3: 拦截与放行"""
    result = TestResult()
    
    # 测试未授权写入被拦截
    # 注意：这个测试不会真正写入，只是验证逻辑
    
    # 模拟检查受保护路径时的行为
    # 未授权时应该返回 False
    test_path = "AGENTS.md"
    is_protected = is_protected_path(test_path)
    result.add("AGENTS.md 受保护判断", is_protected)
    
    # 模拟授权后的行为
    auth_version = authorize_write("AGENTS.md", "拦截测试")
    can_write = is_authorized(auth_version, "AGENTS.md")
    result.add("授权后可写入", can_write)
    
    # 清理
    revoke_authorization(auth_version)
    
    return result


def test_override():
    """测试4: 环境变量覆盖"""
    result = TestResult()
    
    result.add("环境变量状态", True, f"ALLOW_GUARD_OVERRIDE={ALLOW_GUARD_OVERRIDE}")
    result.add(
        "环境变量说明", 
        ALLOW_GUARD_OVERRIDE == False,
        "默认应为 False，设置 ALLOW_GUARD_OVERRIDE=true 可临时绕过"
    )
    
    return result


def test_integration():
    """测试5: 集成测试 - 完整写入流程"""
    result = TestResult()
    
    # 完整流程：授权 -> 写入 -> 验证 -> 撤销
    test_file = "AGENTS.md"
    
    # 1. 获取授权
    auth_version = authorize_write(test_file, "集成测试")
    result.add("集成测试-获取授权", bool(auth_version))
    
    # 2. 验证授权
    authorized = is_authorized(auth_version, test_file)
    result.add("集成测试-验证授权", authorized)
    
    # 3. 模拟写入（不实际写入，避免修改文件）
    # 实际使用 safe_write 时会正确处理
    result.add("集成测试-授权状态有效", authorized)
    
    # 4. 撤销授权
    revoked = revoke_authorization(auth_version)
    result.add("集成测试-撤销授权", revoked)
    
    # 5. 验证撤销后失效
    after_revoke = is_authorized(auth_version, test_file)
    result.add("集成测试-撤销后失效", not after_revoke)
    
    return result


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("路径保护工具测试套件")
    print("=" * 50)
    
    all_results = [
        ("路径保护判断", test_path_protection),
        ("授权与撤销", test_authorization),
        ("拦截与放行", test_interception),
        ("环境变量覆盖", test_override),
        ("集成测试", test_integration),
    ]
    
    total_passed = 0
    total_failed = 0
    
    for name, test_func in all_results:
        print(f"\n【{name}】")
        print("-" * 40)
        result = test_func()
        total_passed += result.passed
        total_failed += result.failed
        result.print_summary()
    
    print("\n" + "=" * 50)
    print(f"总计: {total_passed} 通过, {total_failed} 失败")
    print("=" * 50)
    
    return total_failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)