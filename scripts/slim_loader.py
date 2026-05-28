#!/usr/bin/env python3
"""
Slim Loader — 渐进式技能加载器
根据任务关键词自动选择并只加载对应单个 skill，
输出 system_prompt.txt 给 opencode / GLM-5-Pro 使用。

用法:
  python3 slim_loader.py detect "<用户输入>"     # 检测应加载哪个技能
  python3 slim_loader.py build  "<用户输入>"     # 输出完整 system prompt
  python3 slim_loader.py search "<检索词>"       # 直接检索 wiki，返回相关摘要
"""

import sys
import json
import re
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────────
BASE         = Path(__file__).parent.parent
SKILLS_DIR   = BASE / "skills"
AGENTS_FILE  = BASE / "AGENTS.md"
DB_PATH      = BASE / ".fts_index.db"
# ─────────────────────────────────────────────────────────

# 极简 system prompt 核心（固定 ~200 tokens，不随任务变化）
SLIM_CORE = """你是朱奎烨的个人 LLM Wiki 智能体，遵循 AGENTS.md v2.0。

核心约束（任何情况不可违反）：
1. 不修改 raw/ 目录
2. 任何页面修改后立即执行 python3 scripts/fts_index.py update && python3 scripts/update_graph.py
3. 超过 5 文件的变更需用户书面批准
4. 所有操作记录到 log.md
5. 内容必须贴合求职目标（广州 AI 应用开发 / RAG 工程师）

输出格式：核心内容 / 更新的文件列表 / 归档位置 / 后续建议

执行规范（必须遵守）：
- 每完成一个子步骤立即输出进度，格式：[步骤N] 描述 ✓
- 多步骤任务先生成 /tmp/wiki_task.sh 脚本再一次性执行
- Wiki 同步统一使用：python3 scripts/fts_index.py update && python3 scripts/generate_graph_and_cache.py
- 非致命错误跳过并记录，不要暂停等待确认
- 每次任务结束输出：更新文件列表 / 归档位置 / rtk gain 节省量 / 求职亮点
"""

# 技能路由表：关键词 → skill 文件名
SKILL_ROUTES = {
    "wiki-maintainer": {
        "keywords": ["ingest", "消化", "lint", "健康检查", "图谱", "垃圾回收",
                     "断链", "frontmatter", "索引", "孤立页面", "gc", "repair"],
        "file": "wiki-maintainer.md",
    },
    "context-engineer": {
        "keywords": ["上下文", "context", "token", "压缩", "rag", "检索", "向量",
                     "子智能体", "窗口", "compaction", "multi-agent"],
        "file": "context-engineer.md",
    },
    "prompt-structurer": {
        "keywords": ["提示词", "prompt", "system prompt", "角色", "workflow",
                     "模板", "agent设计", "langgpt"],
        "file": "prompt-structurer.md",
    },
    "theory": {
        "keywords": ["学习", "理论", "拆解", "费曼", "知识点", "原理",
                     "基础", "概念", "理解"],
        "file": None,  # 内联生成，不对应独立 skill 文件
    },
    "practice": {
        "keywords": ["项目", "需求", "技术选型", "踩坑", "复盘", "架构",
                     "开发", "bug", "fastapi", "react", "langchain", "langgraph"],
        "file": None,
    },
    "interview": {
        "keywords": ["简历", "面试", "自我介绍", "投递", "作品集", "复盘",
                     "offer", "hr", "技术面", "薪资"],
        "file": None,
    },
}

# 技能专属附加指令（内联，不需要独立文件）
INLINE_SKILLS = {
    "theory": """
【当前模式：理论补全】
1. 大白话拆解核心原理 + 底层逻辑 + 解决的问题 + 能力边界
2. 结合求职目标明确落地场景
3. 归档到 wiki/my-learning-path/theory/
4. 生成 3 个费曼验证问题
5. 标注项目/面试中的核心坑点
""",
    "practice": """
【当前模式：项目实践】
1. 先讲理论前置，再给落地方案
2. 结合技术栈：FastAPI + React 19 + LangGraph + ChromaDB + GLM-5-Pro
3. 全流程归档到 wiki/my-learning-path/practice/
4. 每次迭代后提炼 STAR 面试话术，同步到 interview/
""",
    "interview": """
【当前模式：求职面试】
1. 基于 Wiki 沉淀生成/优化求职材料
2. 完全贴合意向岗位：广州 AI 应用开发 / RAG 工程师
3. 生成针对性技术面题 + 项目深挖题 + 标准答案
4. 归档到 wiki/my-learning-path/interview/
""",
}


def detect_skill(user_input: str) -> str:
    """返回最匹配的技能 key"""
    text = user_input.lower()
    scores = {}
    for skill_key, cfg in SKILL_ROUTES.items():
        score = sum(1 for kw in cfg["keywords"] if kw in text)
        if score > 0:
            scores[skill_key] = score

    if not scores:
        return "wiki-maintainer"  # 默认维护模式

    return max(scores, key=scores.get)


def load_skill_content(skill_key: str) -> str:
    """加载技能文件内容（或返回内联指令）"""
    cfg = SKILL_ROUTES[skill_key]

    # 内联技能
    if cfg["file"] is None:
        return INLINE_SKILLS.get(skill_key, "")

    skill_path = SKILLS_DIR / cfg["file"]
    if skill_path.exists():
        content = skill_path.read_text(encoding="utf-8")
        # 只保留核心章节，去掉 Skill Metadata（节约 token）
        content = re.sub(r'## \d+\. Skill Metadata.*', '', content, flags=re.DOTALL)
        return content.strip()

    return f"[技能文件未找到: {cfg['file']}]"


def search_wiki(query: str, top_k: int = 5) -> str:
    """使用 FTS 检索 wiki，返回格式化摘要"""
    try:
        import sqlite3
        if not DB_PATH.exists():
            return "[FTS 索引不存在，请先运行: python3 scripts/fts_index.py build]"

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(f"""
            SELECT path, title,
                   snippet(wiki_fts, 3, '▶', '◀', '…', 25) AS snip,
                   bm25(wiki_fts, 0, 2, 4, 1) AS score
            FROM wiki_fts
            WHERE wiki_fts MATCH ?
            ORDER BY score
            LIMIT ?
        """, (query, top_k)).fetchall()
        conn.close()

        if not rows:
            return f"[Wiki 中未找到与 '{query}' 相关的内容]"

        lines = [f"Wiki 检索结果（Top {top_k}）：\n"]
        for r in rows:
            rel_path = Path(r["path"]).name
            lines.append(f"• [{r['title']}]({rel_path}): {r['snip']}")
        return "\n".join(lines)

    except Exception as e:
        return f"[FTS 检索失败: {e}]"


def build_system_prompt(user_input: str) -> str:
    """组装完整 system prompt（精简版）"""
    skill_key = detect_skill(user_input)
    skill_content = load_skill_content(skill_key)

    # 相关 wiki 检索（提取用户输入中的核心词）
    keywords = [w for w in user_input.split() if len(w) > 2][:5]
    wiki_ctx = ""
    if keywords and DB_PATH.exists():
        wiki_ctx = search_wiki(" OR ".join(keywords), top_k=3)
        wiki_ctx = f"\n\n---\n{wiki_ctx}\n---\n"

    prompt = f"""{SLIM_CORE}

---
【已加载技能：{skill_key}】
{skill_content}
{wiki_ctx}
---

用户需求：{user_input}

请严格按照 AGENTS.md 工作流 8 步执行，并在回复末尾输出：
- 更新的文件列表
- 归档位置
- 本次输出对应求职亮点
"""
    return prompt


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "detect" and len(sys.argv) > 2:
        user_input = " ".join(sys.argv[2:])
        skill = detect_skill(user_input)
        print(f"检测到技能: {skill}")

    elif cmd == "build" and len(sys.argv) > 2:
        user_input = " ".join(sys.argv[2:])
        prompt = build_system_prompt(user_input)
        out_path = Path("/tmp/system_prompt.txt")
        out_path.write_text(prompt, encoding="utf-8")
        print(prompt)
        print(f"\n[已保存到 {out_path}]")

    elif cmd == "search" and len(sys.argv) > 2:
        query = " ".join(sys.argv[2:])
        print(search_wiki(query))

    else:
        print(__doc__)
