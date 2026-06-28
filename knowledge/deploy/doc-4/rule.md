# Kubernetes 部署管理 — 规则

## 规则列表

| 规则 | 说明 | 优先级 | 强制 |
|------|------|--------|------|
| DEP-K8S-001 | 所有工作负载必须设置 resource requests 和 limits | P0 | 是 |
| DEP-K8S-002 | 所有 Deployment 必须配置 liveness 和 readiness probe | P0 | 是 |
| DEP-K8S-003 | 敏感信息使用 Sealed Secrets / External Secrets，不直接使用 Secret | P0 | 是 |
| DEP-K8S-004 | Pod 安全上下文禁止 privileged 模式，只读根文件系统 | P0 | 是 |
| DEP-K8S-005 | Ingress 必须配置 TLS 终止和请求限制 | P0 | 是 |
| DEP-K8S-006 | 每个 Namespace 必须设置 ResourceQuota 和 NetworkPolicy | P0 | 是 |
| DEP-K8S-007 | 部署策略使用 RollingUpdate 或 BlueGreen，禁止 Recreate | P1 | 是 |

## 详细说明

### DEP-K8S-001（P0）
所有工作负载必须设置 resource requests 和 limits

### DEP-K8S-002（P0）
所有 Deployment 必须配置 liveness 和 readiness probe

### DEP-K8S-003（P0）
敏感信息使用 Sealed Secrets / External Secrets，不直接使用 Secret

### DEP-K8S-004（P0）
Pod 安全上下文禁止 privileged 模式，只读根文件系统

### DEP-K8S-005（P0）
Ingress 必须配置 TLS 终止和请求限制

### DEP-K8S-006（P0）
每个 Namespace 必须设置 ResourceQuota 和 NetworkPolicy

### DEP-K8S-007（P1）
部署策略使用 RollingUpdate 或 BlueGreen，禁止 Recreate

