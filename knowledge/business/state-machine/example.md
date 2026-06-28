```yaml
# KPI 指标体系配置
north_star: 活跃项目数

tier1:
  - name: 新增注册量
    formula: COUNT(DISTINCT user_id) WHERE signup_date = TODAY
    source: user_events.signup
    target: 5000/日
    frequency: 日
  - name: 核心功能 MAU
    formula: COUNT(DISTINCT user_id) WHERE event_name = "core_action" AND date >= DATE_ADD(TODAY, -30)
    source: product_events.core_action
    target: 50万
    frequency: 月
  - name: 付费转化率
    formula: paid_users / registered_users * 100
    source: billing.payments / user_events.signup
    target: 5%
    frequency: 周
  - name: 用户留存率(D30)
    formula: users_active_day30 / users_signup * 100
    source: user_events.activity
    target: 40%
    frequency: 月
  - name: NPS
    formula: promoters - detractors
    source: survey.nps
    target: 50
    frequency: 月
```