# CI/CD 流水线规范 — FAQ

## Q1: Jenkins vs GitHub Actions vs GitLab CI？
GitHub Actions（推荐）：与 GitHub 深度集成、Action 生态丰富、配置简单。GitLab CI：内置容器注册中心、Kubernetes 集成好。Jenkins：高度可定制、插件生态最大、但维护成本高。

## Q2: 如何优化 CI 速度？
① 构建缓存（依赖缓存、Docker 缓存层）② 并行执行（分段并行测试）③ 增量构建（只编译变更部分）④ 按需运行（前端变更时只跑前端测试）⑤ 使用高性能 Runner。
