# 监控与告警规范 — FAQ

## Q1: Prometheus vs Datadog vs Grafana Cloud？
Prometheus + Grafana（推荐）：开源、自托管、成本可控、生态丰富。Datadog：全托管、集成最全、但成本高。Grafana Cloud：托管的 Prometheus + Loki + Tempo 组合。

## Q2: 告警阈值怎么设定？
基于历史数据设定基线，基线值 × 1.5-2 倍作为告警阈值。例如系统正常 P95 延迟 200ms，设置告警阈值为 400ms 持续 5 分钟。避免使用固定值，使用动态基线更好。
