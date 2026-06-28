# RAG 系统设计 — FAQ

## Q1: Chunk Size 怎么设置？
经验值：256-512 tokens（英文）、512-1024 tokens（中文）。根据文档类型调整：FAQ 类<100 tokens、技术文档 300-500 tokens、长文 500-800 tokens。关键原则：确保每个 Chunk 语义完整。

## Q2: RAG 检索不到正确文档怎么办？
① 优化分块策略（重叠窗口 10-20%）② 增加元数据过滤（日期、类别、标签）③ 使用 Query Rewrite（将用户问题改写为更适合检索的形式）④ 增加 Hybrid Search 权重⑤ 使用 RAG Fusion（多查询合并结果）。
