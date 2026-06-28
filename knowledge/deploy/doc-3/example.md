```markdown
# 发布回滚方案: Order Service v2.3.0

## 回滚条件（满足任一即回滚）
- [ ] 错误率较基线上升 > 2%（连续 3 分钟）
- [ ] P95 响应时间 > 2s（连续 5 分钟）
- [ ] 用户反馈渠道出现 10+ 同类投诉
- [ ] 关键业务指标（下单成功率）下降 > 5%

## 回滚流程

### 步骤 1: 判定（5 分钟内）
值班人员确认触发条件 → 通知发布经理 → 发布经理决策

### 步骤 2: 执行（3 分钟内）
```bash
# 自动回滚脚本
kubectl rollout undo deployment/order-service -n production
kubectl rollout status deployment/order-service -n production --timeout=120s
```

### 步骤 3: 验证（10 分钟内）
- [ ] 确认新 Pod 运行正常
- [ ] 错误率回到基线水平
- [ ] 核心 API 响应正常
- [ ] 数据库连接池稳定
- [ ] 主动测试下单流程通过

### 步骤 4: 通知
- 发布群: @all 回滚完成
- 相关方: 邮件 + IM 通知
- 值班: 继续监控 30 分钟

## 数据库降级
```sql
-- 如果 v2.3.0 新增了字段
ALTER TABLE orders DROP COLUMN IF EXISTS new_feature_flag;
-- 如果 v2.3.0 修改了索引
DROP INDEX IF EXISTS idx_orders_new_feature ON orders;
```

## 根因分析模板（回滚后 24h 内完成）
### 问题描述
### 影响范围
### 根因分析
### 改进措施
### 责任人
```