# 容器化部署规范 — 规则

## 规则列表

| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| DEP-CNT-001 | Dockerfile 必须使用多阶段构建（Builder → Runner） | P0 | 是 |
| DEP-CNT-002 | 基础镜像使用官方 Alpine 或 Distroless 发行版 | P0 | 是 |
| DEP-CNT-003 | 容器内禁止以 root 用户运行应用 | P0 | 是 |
| DEP-CNT-004 | 镜像必须通过安全扫描（Trivy/Clair）无高危漏洞 | P0 | 是 |
| DEP-CNT-005 | 环境变量通过运行平台注入，不在镜像中硬编码 | P0 | 是 |
| DEP-CNT-006 | 容器设置资源限制（CPU/Memory requests & limits） | P0 | 是 |
| DEP-CNT-007 | 应用日志写入 stdout/stderr，由容器运行时收集 | P0 | 是 |

## 详细说明

### DEP-CNT-001（P0）
Dockerfile 必须使用多阶段构建（Builder → Runner）

### DEP-CNT-002（P0）
基础镜像使用官方 Alpine 或 Distroless 发行版

### DEP-CNT-003（P0）
容器内禁止以 root 用户运行应用

### DEP-CNT-004（P0）
镜像必须通过安全扫描（Trivy/Clair）无高危漏洞

### DEP-CNT-005（P0）
环境变量通过运行平台注入，不在镜像中硬编码

### DEP-CNT-006（P0）
容器设置资源限制（CPU/Memory requests & limits）

### DEP-CNT-007（P0）
应用日志写入 stdout/stderr，由容器运行时收集

