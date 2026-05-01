---
title: LLM Wiki RAG化自我优化方案
type: synthesis
tags: [RAG, wiki, self-optimization, 知识库]
sources: [RAG混合检索核心原理]
created: 2026-05-01
updated: 2026-05-01
---

# LLM Wiki RAG化自我优化方案

## 一、当前Wiki架构

```
当前检索方式：
- wikilinks图关系检索（index-cache.json）
- 文件名匹配
- 纯图结构，无语义理解能力
```

**痛点**：
1. 只能通过链接关系查找，无法语义搜索内容
2. 用户提问无法直接得到答案，需手动翻文档
3. 跨领域内容关联依赖人工维护

---

## 二、RAG化升级架构

```
用户自然语言提问
       ↓
┌──────────────────┐
│   语义理解层     │
│  (embedding向量化)│
└────────┬─────────┘
         ↓
┌──────────────────┐
│   混合检索层     │
│ 向量检索+BM25    │
│    + 图关系      │
└────────┬─────────┘
         ↓
┌──────────────────┐
│   答案生成层     │
│  (LLM生成答案)   │
└────────┬─────────┘
         ↓
    直接返回答案
```

---

## 三、落地方案

### 第1步：构建向量索引

```python
# scripts/wiki_vector_index.py
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import json

WIKI_PATH = "/mnt/d/projects/wiki/wiki"
VECTOR_PATH = "/mnt/d/projects/wiki/wiki/.vector_store"

def build_vector_index():
    """构建Wiki向量索引"""
    documents = []
    
    # 遍历所有md文件
    for root, dirs, files in os.walk(WIKI_PATH):
        # 跳过系统目录
        if any(x in root for x in ['.git', '.obsidian', 'scripts', 'output', 'raw']):
            continue
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 提取frontmatter后的正文
                    if '---' in content:
                        content = content.split('---', 2)[-1]
                    documents.append({
                        'id': filepath,
                        'content': content,
                        'source': os.path.relpath(filepath, WIKI_PATH)
                    })
    
    # 分块
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    texts = [d['content'] for d in documents]
    chunks = text_splitter.split_texts(texts)
    
    # 向量化并存储
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_texts(
        chunks,
        embedding=embeddings,
        persist_directory=VECTOR_PATH
    )
    vectorstore.persist()
    print(f"向量索引构建完成：{len(chunks)} 个文本块")

if __name__ == "__main__":
    build_vector_index()
```

### 第2步：实现混合检索

```python
# scripts/wiki_hybrid_search.py
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from rank_bm25 import BM25Okapi
import json
import os

class WikiHybridSearch:
    def __init__(self, vector_path, wiki_path):
        self.vectorstore = Chroma(
            persist_directory=vector_path,
            embedding_function=OpenAIEmbeddings()
        )
        self.wiki_path = wiki_path
        self._init_bm25()
    
    def _init_bm25(self):
        """初始化BM25"""
        documents = []
        for root, dirs, files in os.walk(self.wiki_path):
            if any(x in root for x in ['.git', '.obsidian', 'scripts', 'output', 'raw']):
                continue
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if '---' in content:
                            content = content.split('---', 2)[-1]
                        documents.append(content)
        
        self.tokenized_docs = [doc.split() for doc in documents]
        self.bm25 = BM25Okapi(self.tokenized_docs)
    
    def search(self, query, top_k=5):
        # 向量检索
        vector_results = self.vectorstore.similarity_search_with_score(query, k=top_k)
        
        # BM25检索
        bm25_results = self.bm25.search(query.split(), top_k)
        
        # RRF融合
        doc_scores = {}
        k = 60
        for i, (doc, _) in enumerate(vector_results):
            doc_id = doc.metadata.get('source', f'doc_{i}')
            doc_scores[doc_id] = doc_scores.get(doc_id, 0) + 1/(k + i)
        
        for i, (score, _) in enumerate(bm25_results):
            doc_id = f'bm25_{i}'
            doc_scores[doc_id] = doc_scores.get(doc_id, 0) + 1/(k + i)
        
        # 排序返回
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]
```

### 第3步：集成LLM问答

```python
# scripts/wiki_qa.py
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from wiki_hybrid_search import WikiHybridSearch

class WikiQA:
    def __init__(self, vector_path, wiki_path):
        self.search = WikiHybridSearch(vector_path, wiki_path)
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        
        # 构建QA chain
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.search.vectorstore.as_retriever()
        )
    
    def answer(self, question):
        """回答用户问题"""
        return self.qa.run(question)

# 使用示例
if __name__ == "__main__":
    qa = WikiQA(
        vector_path="/mnt/d/projects/wiki/wiki/.vector_store",
        wiki_path="/mnt/d/projects/wiki/wiki"
    )
    
    while True:
        question = input("请输入问题（输入q退出）：")
        if question == 'q':
            break
        answer = qa.answer(question)
        print(f"\n答案：{answer}\n")
```

---

## 四、可实现的增强功能

| 功能 | 描述 | 技术方案 |
|------|------|----------|
| **语义搜索** | 用自然语言搜索Wiki内容 | Embedding + 向量检索 |
| **智能问答** | 直接回答用户的知识库问题 | RAG + LLM生成 |
| **内容推荐** | 基于当前阅读内容推荐相关文档 | 向量相似度 |
| **自动摘要** | 对长文档自动生成摘要 | LLM提取 |
| **关联发现** | 自动发现跨领域的知识关联 | 图关系 + 语义 |

---

## 五、优先级与时间规划

### 短期（1-2周）
- [ ] 构建Wiki向量索引
- [ ] 实现基础语义搜索

### 中期（1个月）
- [ ] 集成LLM问答
- [ ] 实现混合检索（向量+BM25）

### 长期（2-3个月）
- [ ] 自动摘要功能
- [ ] 智能内容推荐
- [ ] 知识关联发现

---

## 六、预期效果

- 用户可以用自然语言直接查询Wiki内容
- 无需手动翻阅文档，直接获得答案
- 语义相似的相关内容自动推荐
- 跨领域知识自动关联

---

## References

- [[my-learning-path/theory/rag-theory|RAG技术原理]]
- [[my-learning-path/practice/technical-weapons|我的技术武器库]]