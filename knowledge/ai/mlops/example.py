```python
# MLflow 实验跟踪配置
import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri("http://mlflow-server:5000")
mlflow.set_experiment("customer-churn-prediction")

# 训练 Pipeline
with mlflow.start_run(run_name="v2.1.0-xgboost"):
    # 记录参数
    mlflow.log_params({
        "model_type": "XGBoost",
        "learning_rate": 0.05,
        "max_depth": 6,
        "n_estimators": 500,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "data_version": "v2024-01-15"
    })

    # 训练模型
    model = xgb.train(params, dtrain, num_boost_round=500)

    # 评估
    y_pred = model.predict(dtest)
    metrics = {
        "auc": roc_auc_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred > 0.5),
        "recall": recall_score(y_test, y_pred > 0.5),
        "f1": f1_score(y_test, y_pred > 0.5)
    }

    # 记录指标
    mlflow.log_metrics(metrics)

    # 记录模型
    mlflow.xgboost.log_model(model, "model")

    # 记录特征重要性
    mlflow.log_artifact("feature_importance.png")

# 模型注册
client = MlflowClient()

# 模型从 Staging 晋升到 Production
client.transition_model_version_stage(
    name="customer-churn-model",
    version=5,
    stage="Production"
)

# 模型监控：数据漂移检测
# 使用 evidently.ai 或 whylogs 生成监控报告
# 如果 PSI > 0.2，自动创建 JIRA 工单触发重新训练
```