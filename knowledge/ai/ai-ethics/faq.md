# AI 伦理规范 — FAQ

## Q1: 如何检测 AI 偏见？
在不同子群体上分别评估模型准确率。如果某个群体的准确率显著低于平均，说明存在偏见。使用公平性指标：Demographic Parity、Equal Opportunity、Equalized Odds。

## Q2: AI 的「黑盒」问题怎么解决？
使用可解释 AI 工具：SHAP（特征重要性）、LIME（局部解释）、Grad-CAM（视觉解释）。对于高风险决策，使用可解释性强的模型（如决策树、逻辑回归）作为备选。
