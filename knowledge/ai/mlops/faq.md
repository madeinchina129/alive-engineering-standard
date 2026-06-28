# MLOps 规范 — FAQ

## Q1: MLflow vs Kubeflow vs Airflow？
MLflow：实验跟踪 + 模型注册，轻量级，适合团队起步。Kubeflow：端到端 ML Pipeline 平台，K8s 原生，适合大规模部署。Airflow：通用工作流编排，适合复杂的 ETL + 训练混合流程。通常组合使用：MLflow + 任意的 Pipeline 工具。

## Q2: 模型漂移如何检测？
Data Drift：使用统计检验（KS 检验/PSI）比较当前数据和训练数据的分布差异。Concept Drift：监控模型预测分布和实际标签分布的变化。阈值设定：PSI > 0.2 或 KS p-value < 0.05 触发告警。
