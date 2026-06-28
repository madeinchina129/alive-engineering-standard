```python
# 数据分析示例：用户留存分析
import pandas as pd
import matplotlib.pyplot as plt

# 1. 数据加载
user_activity = pd.read_csv('user_activity.csv')
print(f'数据范围: {user_activity["date"].min()} ~ {user_activity["date"].max()}')
print(f'用户总量: {user_activity["user_id"].nunique()}')

# 2. 留存率计算
def cohort_retention(df, period=7):
    cohort_data = df.groupby('cohort_date')['user_id'].nunique()
    retention = {}
    for date in cohort_data.index[:10]:
        base_users = df[df['cohort_date'] == date]['user_id'].nunique()
        retained = df[(df['cohort_date'] == date) & (df['days_since_signup'] >= period)]['user_id'].nunique()
        retention[date] = retained / base_users
    return pd.Series(retention)

retention_7d = cohort_retention(user_activity, 7)
print(f'7日留存率: {retention_7d.mean():.1%}')

# 3. 可视化
plt.figure(figsize=(12, 6))
retention_7d.plot(marker='o')
plt.title('7日留存率趋势')
plt.xlabel('注册日期')
plt.ylabel('留存率')
plt.grid(True, alpha=0.3)
plt.savefig('retention_trend.png', dpi=150)
```