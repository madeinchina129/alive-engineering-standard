# AI Agent 设计规范 — FAQ

## Q1: Plan-and-Execute vs ReAct？
ReAct：推理和行动交错进行，适合逐步发现和解决的问题。Plan-and-Execute：先制定完整计划再执行，适合步骤明确的任务。复杂任务推荐 Plan-and-Execute 分解为子任务，每个子任务内部用 ReAct。

## Q2: Agent 记忆怎么管理？
三层记忆：① 短期记忆（当前会话上下文，全部保留）② 长期记忆（跨会话关键信息，用向量数据库存储）③ 工作记忆（当前步骤的中间结果，步完成后清理）。使用 MemGPT/Letta 等框架管理记忆。
