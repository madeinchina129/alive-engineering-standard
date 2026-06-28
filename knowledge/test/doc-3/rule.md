# 集成测试规范 — 规则

## 规则列表

| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| TST-IT-001 | 集成测试必须使用 Testcontainers 或 Docker Compose 管理依赖服务 | P0 | 是 |
| TST-IT-002 | 每次测试运行前重建测试数据库（Flyway/Liquibase migrate） | P0 | 是 |
| TST-IT-003 | 外部 API 调用使用 WireMock 录制/回放模式 | P0 | 是 |
| TST-IT-004 | 集成测试不要使用 @SpringBootTest 全量启动，只加载需要的上下文 | P1 | 是 |
| TST-IT-005 | 集成测试运行时间不应超过 10 分钟 | P1 | 是 |

## 详细说明

### TST-IT-001（P0）
集成测试必须使用 Testcontainers 或 Docker Compose 管理依赖服务

### TST-IT-002（P0）
每次测试运行前重建测试数据库（Flyway/Liquibase migrate）

### TST-IT-003（P0）
外部 API 调用使用 WireMock 录制/回放模式

### TST-IT-004（P1）
集成测试不要使用 @SpringBootTest 全量启动，只加载需要的上下文

### TST-IT-005（P1）
集成测试运行时间不应超过 10 分钟

