# Kubernetes 部署管理

## 概述
Kubernetes 是容器编排的事实标准。本规范涵盖了集群架构、Pod 配置、服务发现、Ingress 路由、配置管理和资源调度等生产级配置标准。

## 核心原则
1. 声明式管理：所有资源通过 YAML 声明，不手动操作
2. 自愈优先：利用 K8s 健康检查和自动重启机制
3. 渐进式发布：使用 Rolling Update / Blue-Green / Canary 策略
4. 资源隔离：通过 Namespace 和 ResourceQuota 实现租户隔离

## 适用范围
适用于本项目中所有相关场景。
