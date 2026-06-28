# GraphQL API 设计规范 — FAQ

## Q1: GraphQL 和 REST 怎么选？
GraphQL 适合：数据聚合层（BFF）、前端驱动的快速迭代、多客户端差异需求。REST 适合：简单 CRUD、缓存友好、工具链成熟、第三方 API。实践中常混合使用两种方式。

## Q2: GraphQL 的性能问题怎么处理？
① DataLoader 解决 N+1 ② Persisted Queries 减少传输 ③ @defer/@stream 指令优化大数据加载 ④ CDN 缓存查询结果 ⑤ 使用 Apollo Studio 监控慢查询。
