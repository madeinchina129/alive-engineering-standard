```python
# RAG Pipeline 核心实现

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.retrievers import EnsembleRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from sentence_transformers import CrossEncoder

# 1. 文档分块
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=64,  # 10-20% 重叠
    separators=["\n## ", "\n### ", "\n\n", "\n", "。", "！", "？", " ", ""],
    length_function=len
)
chunks = text_splitter.split_documents(documents)

# 2. 向量存储
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 3. 混合检索（关键词 + 向量）
bm25_retriever = BM25Retriever.from_documents(chunks)
bm25_retriever.k = 5

vector_retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.3, 0.7]
)

# 4. 重排序
reranker = CrossEncoderReranker(
    model=CrossEncoder("BAAI/bge-reranker-v2-m3"),
    top_n=3
)

# 5. 生成
query = "如何配置数据库连接池？"
retrieved = ensemble_retriever.get_relevant_documents(query)
reranked = reranker.compress_documents(
    documents=retrieved,
    query=query
)

context = "\n\n---\n\n".join([d.page_content for d in reranked])
prompt = f"""请基于以下知识回答问题。如果知识库中没有相关信息，请如实说不知道。

知识：
{context}

问题：{query}

请引用知识来源（在引用处标注 [来源：文档ID-XX]）。
"""
```