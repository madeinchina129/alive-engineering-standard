# Kubernetes 部署管理 — FAQ

## Q1: Service 类型选型？
ClusterIP：集群内访问（微服务间通信）。NodePort：外部调试/测试。LoadBalancer：对外暴露服务（云厂商）。Ingress：HTTP/HTTPS 七层路由（对外统一入口）。

## Q2: Pod 健康检查配置多少合适？
liveness probe：检测应用是否存活（如进程死锁）。initialDelaySeconds: 30-60s，periodSeconds: 10-30s，failureThreshold: 3-5。readiness probe：检测应用是否可接受流量。initialDelaySeconds: 5-10s，periodSeconds: 5-10s。
