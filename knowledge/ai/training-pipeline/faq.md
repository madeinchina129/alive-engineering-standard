# 模型训练流水线 — FAQ

## Q1: 分布式训练的并行策略？
Data Parallel（数据并行）：每个 GPU 处理不同 batch，梯度同步。Model Parallel（模型并行）：不同 GPU 处理模型不同层。Pipeline Parallel（流水线并行）：将模型按层分组到不同 GPU。3D Parallel 是三种组合。

## Q2: GPU 利用率不高怎么办？
① 增大 batch size ② 使用 DataLoader 的 num_workers 预加载 ③ 使用梯度累积 ④ 检查是否存在 CPU 瓶颈（数据加载成为瓶颈）⑤ 使用 NVIDIA DALI 加速数据加载。
