# 性能测试规范 — FAQ

## Q1: JMeter 还是 Locust 还是 k6？
k6（推荐）：Go 开发、配置简单、CI 集成好、支持 JavaScript 脚本。JMeter：老牌工具、功能全面、但资源占用大。Locust：Python 编写、分布式支持好。

## Q2: 性能测试在 CI 中运行吗？
轻量级基准测试在每次 PR 时运行（3-5 分钟），全量性能测试在预发布环境每晚运行一次。
