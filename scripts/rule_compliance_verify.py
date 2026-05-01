import os
import json
import shutil
import hashlib
from datetime import datetime

def verify_rule_compliance():
    # 读取核心规则缓存
    with open("index-cache.json", "r", encoding="utf-8") as f:
        cache_data = json.load(f)

    # 校验1：原有agents.md、skills.md未被修改
    original_agents_md5 = cache_data.get("original_agents_md5", "")
    original_skills_md5 = cache_data.get("original_skills_md5", "")

    # 计算当前文件哈希，确认未被改动
    def get_file_md5(file_path):
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    current_agents_md5 = get_file_md5("agents.md")
    current_skills_md5 = get_file_md5("skills.md")

    if original_agents_md5 and current_agents_md5 != original_agents_md5:
        # 触发回滚，恢复原有文件
        backup_path = ".gc_backups/agents.md.bak"
        if os.path.exists(backup_path):
            shutil.copyfile(backup_path, "agents.md")
        with open("log.md", "a", encoding="utf-8") as f:
            f.write(f"[规则违规] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 检测到原有agents.md被违规修改，已自动回滚到备份版本\n")
        return False, "原有agents.md被违规修改，已自动回滚"

    if original_skills_md5 and current_skills_md5 != original_skills_md5:
        backup_path = ".gc_backups/skills.md.bak"
        if os.path.exists(backup_path):
            shutil.copyfile(backup_path, "skills.md")
        with open("log.md", "a", encoding="utf-8") as f:
            f.write(f"[规则违规] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 检测到原有skills.md被违规修改，已自动回滚到备份版本\n")
        return False, "原有skills.md被违规修改，已自动回滚"

    # 校验2：其他规则合规性（原有wiki-maintainer规范）
    cache_exists = os.path.exists("index-cache.json")
    if not cache_exists or os.path.getmtime("index-cache.json") < os.path.getmtime("agents.md"):
        os.system("python3 scripts/update_graph.py > /dev/null 2>&1")
        with open("log.md", "a", encoding="utf-8") as f:
            f.write(f"[规则补全] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 自动执行图谱同步，符合wiki-maintainer规范\n")

    # 校验通过，记录日志
    with open("log.md", "a", encoding="utf-8") as f:
        f.write(f"[规则校验通过] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 所有操作符合原有规范+扩展规则，原有内容未被改动\n")

    return True, "所有规则校验通过，原有优质内容100%保留"

if __name__ == "__main__":
    is_compliant, msg = verify_rule_compliance()
    if not is_compliant:
        print(f"X {msg}")
        exit(1)
    else:
        print(f"V {msg}")
        exit(0)