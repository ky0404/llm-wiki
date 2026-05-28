---
title: RAG From Scratch 学习笔记
type: practice
tags: [RAG, LangChain, 向量数据库, 检索增强生成]
version: 1.0
author: 朱奎烨
created: 2026-05-27
updated: 2026-05-27
dependencies:
  - concepts/rag.md
  - concepts/llm.md
---

# RAG From Scratch 学习笔记

> 教程来源：https://github.com/langchain-ai/rag-from-scratch
> 配套视频：https://youtube.com/playlist?list=PLfaIDFEXuae2LXb1_PKyVJiQ23ZztA0x

## 一、整体架构

RAG 核心流程：
```
┌─────────────────────────────────────────────────────────────┐
│  INDEXING (离线)                                            │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │  Load    │ → │  Split   │ → │  Embed   │ → │ Vector   │ │
│  │ Documents│   │  (Chunk) │   │ (Vectors)│   │  Store   │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
├─────────────────────────────────────────────────────────────┤
│  RETRIEVAL & GENERATION (在线)                              │
│  ┌──────────┐   ┌──────────┐   ┌────────┐   ┌───────────┐ │
│  │  Query   │ → │ Retrieve │ → │ Prompt │ → │    LLM    │ │
│  │ (User)   │   │  (Top-K) │   │Template│   │  Generate │ │
│  └──────────┘   └──────────┘   └────────┘   └───────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、第 1-4 阶段：基础 RAG 流程

### 2.1 环境配置

```bash
pip install langchain_community tiktoken langchain-openai langchainhub chromadb langchain
```

```python
import os
os.environ['OPENAI_API_KEY'] = 'your-key'
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_API_KEY'] = 'your-key'
```

### 2.2 文档加载 (Part 2)

```python
import bs4
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()
```

### 2.3 文本分块 (Part 2)

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 基于 token 精确控制
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=300, 
    chunk_overlap=50
)
splits = text_splitter.split_documents(docs)
```

**分块策略选择**：
| 分块方法 | 适用场景 |
|----------|----------|
| RecursiveCharacterTextSplitter | 通用，推荐 |
| MarkdownHeaderTextSplitter | Markdown 文档 |
| PythonCodeTextSplitter | 代码文件 |

### 2.4 嵌入与向量存储 (Part 2)

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 嵌入向量
embeddings = OpenAIEmbeddings()  # text-embedding-ada-002, 1536维

# 存入向量数据库
vectorstore = Chroma.from_documents(
    documents=splits, 
    embedding=OpenAIEmbeddings()
)

# 获取检索器
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
```

### 2.5 检索 (Part 3)

```python
# Top-K 检索
docs = retriever.invoke("What is Task Decomposition?")
```

### 2.6 生成 (Part 4)

```python
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Prompt 模板
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# 格式化文档
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# LCEL 链式调用
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 执行
rag_chain.invoke("What is Task Decomposition?")
```

---

## 三、第 5-9 阶段：高级查询转换

### 3.1 Multi Query（多查询）

**原理**：生成多个同义查询，扩大检索覆盖面

```python
from langchain.load import dumps, loads
from operator import itemgetter

# 生成多查询的提示
template = """You are an AI language model assistant. Your task is to generate five 
different versions of the given user question to retrieve relevant documents from a vector 
database. Provide these alternative questions separated by newlines.
Original question: {question}"""
prompt_perspectives = ChatPromptTemplate.from_template(template)

# 生成查询链
generate_queries = (
    prompt_perspectives 
    | ChatOpenAI(temperature=0) 
    | StrOutputParser() 
    | (lambda x: x.split("\n"))
)

# 去重函数
def get_unique_union(documents: list[list]):
    flattened_docs = [dumps(doc) for sublist in documents for doc in sublist]
    unique_docs = list(set(flattened_docs))
    return [loads(doc) for doc in unique_docs]

# 完整检索链
retrieval_chain = generate_queries | retriever.map() | get_unique_union
docs = retrieval_chain.invoke({"question": "What is task decomposition?"})
```

### 3.2 RAG-Fusion（RRF 重排序）

**原理**：使用互惠排名融合算法对多查询结果重排序

```python
def reciprocal_rank_fusion(results: list[list], k=60):
    fused_scores = {}
    for docs in results:
        for rank, doc in enumerate(docs):
            doc_str = dumps(doc)
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
            fused_scores[doc_str] += 1 / (rank + k)
    
    reranked = [
        (loads(doc), score)
        for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    ]
    return reranked

retrieval_chain_rag_fusion = generate_queries | retriever.map() | reciprocal_rank_fusion
```

**RRF 公式**：`score = 1 / (rank + k)`，k 默认 60

### 3.3 Decomposition（查询分解）

**原理**：将复杂问题拆解为子问题

```python
# 子问题生成
template = """Generate multiple sub-questions related to: {question}
Output (3 queries):"""
prompt_decomposition = ChatPromptTemplate.from_template(template)

generate_sub_questions = prompt_decomposition | llm | StrOutputParser() | (lambda x: x.split("\n"))

# 独立回答每个子问题，最后合成
def retrieve_and_rag(question):
    sub_questions = generate_sub_questions.invoke({"question": question})
    answers = []
    for sq in sub_questions:
        docs = retriever.invoke(sq)
        answer = (prompt | llm | StrOutputParser()).invoke({"context": docs, "question": sq})
        answers.append(answer)
    return answers, sub_questions
```

### 3.4 Step Back（回退提示）

**原理**：先抽象为更通用的背景问题，再回答具体问题

```python
# Few-shot 回退提示
examples = [
    {"input": "Could the members of The Police perform lawful arrests?",
     "output": "what can the members of The Police do?"},
]

prompt_step_back = ChatPromptTemplate.from_messages([
    ("system", "Step back and paraphrase to a more generic question."),
    FewShotChatMessagePromptTemplate(examples=examples, example_prompt=example_prompt),
    ("user", "{question}"),
])

generate_step_back = prompt_step_back | llm | StrOutputParser()

# 双重检索
chain = {
    "normal_context": retriever,
    "step_back_context": generate_step_back | retriever,
    "question": lambda x: x["question"],
} | response_prompt | llm | StrOutputParser()
```

### 3.5 HyDE（假设文档嵌入）

**原理**：用 LLM 生成"假想答案"来引导检索

```python
# 生成假设文档
template = """Please write a scientific paper passage to answer the question
Question: {question}
Passage:"""
prompt_hyde = ChatPromptTemplate.from_template(template)

generate_hypothetical = prompt_hyde | llm | StrOutputParser()

# 用假设文档检索真实文档
retrieval_chain = generate_hypothetical | retriever
retrieved_docs = retrieval_chain.invoke({"question": question})

# 最终生成
final_answer = (prompt | llm | StrOutputParser()).invoke({"context": retrieved_docs, "question": question})
```

---

## 四、对比你的项目

| 特性 | rag-from-scratch | 你的项目（媛心烨语）|
|------|------------------|---------------------|
| 向量数据库 | Chroma | Chroma ✅ |
| 检索方式 | 单一向量检索 | 三混合 RAG（Vector + Graph + BM25）✅ |
| 查询优化 | 无 | Self-RAG 路由 ✅ |
| Reranking | 无 | 可借鉴 RRF |
| 评估 | 基础 | Langfuse 全链路 ✅ |

**你可以借鉴的**：
1. **Multi Query**：当前只用了单一查询，可以尝试生成多版本查询
2. **RRF 重排序**：你的项目还没用 RRF，可以考虑
3. **HyDE**：可以用假设文档增强检索

---

## 五、学习路线建议

### 第一阶段：环境搭建（1天）
```bash
mkdir ~/rag-learning && cd ~/rag-learning
git clone https://github.com/langchain-ai/rag-from-scratch.git
python -m venv venv && source venv/bin/activate
pip install jupyter notebook langchain langchain-openai chromadb
jupyter notebook
```

### 第二阶段：Notebook 实操（3-5天）
- `rag_from_scratch_1_to_4.ipynb` → 基础流程
- `rag_from_scratch_5_to_9.ipynb` → 查询转换进阶

### 第三阶段：迁移到项目（2-3天）
- 挑选适合你项目的技术（Multi Query + RRF）
- 在项目中实现并测试

---

## 六、参考资源

- [LangChain MultiQueryRetriever](https://python.langchain.com/docs/modules/data_connection/retrievers/MultiQueryRetriever)
- [HyDE 论文](https://arxiv.org/abs/2212.10496)
- [Step-Back Prompting 论文](https://arxiv.org/pdf/2310.06117.pdf)
- [RAG-Fusion 博客](https://towardsdatascience.com/forget-rag-the-future-is-rag-fusion-1147298d8ad1)

---

## 七、面试相关

### 常见问题

1. **RAG 的核心流程是什么？**
   索引构建 → 检索 → 生成

2. **为什么要做文本分块？**
   控制 token 数量、提升检索精度、避免超过 LLM 上下文限制

3. **Multi Query 和 RAG-Fusion 的区别？**
   RAG-Fusion 在 Multi Query 基础上加了 RRF 重排序

4. **HyDE 的原理？**
   用 LLM 生成的假设文档去检索，包含更多领域术语，提升召回

5. **什么场景下用查询分解？**
   复杂多维度问题，需要综合多个子问题的答案