import os
import json

def preload_core_rules():
    # 读取原有agents.md全部内容+新增扩展规则
    with open("agents.md", "r", encoding="utf-8") as f:
        agents_full_content = f.read()

    # 读取原有skills.md全部内容+新增扩展技能
    with open("skills.md", "r", encoding="utf-8") as f:
        skills_full_content = f.read()

    # 提取高信号核心规则（压缩token，不超过92%窗口阈值）
    core_rules = f"""
    【核心规则预加载】
    1. 必须严格遵循agents.md全部原有规范+用户专属永久执行扩展规则
    2. 必须严格遵循skills.md全部原有技能库+用户专属落地扩展技能
    3. 所有操作必须服务于使用者校招求职目标，自动归档到my-learning-path/对应目录
    4. 上下文窗口严禁超过92%阈值，违规操作自动回滚
    5. 原有wiki-maintainer、context-engineer、prompt-structurer规范全部生效
    """

    # 缓存核心规则，供上下文注入
    with open("index-cache.json", "r", encoding="utf-8") as f:
        cache_data = json.load(f)

    cache_data["core_rules_cache"] = core_rules
    cache_data["agents_full_content"] = agents_full_content
    cache_data["skills_full_content"] = skills_full_content

    with open("index-cache.json", "w", encoding="utf-8") as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)

    print("核心规则预加载完成，原有内容100%保留，扩展规则已生效")
    return core_rules

if __name__ == "__main__":
    preload_core_rules()