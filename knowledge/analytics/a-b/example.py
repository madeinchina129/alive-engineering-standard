```python
# A/B 测试分析示例
import numpy as np
from scipy import stats

# 实验数据
control = {'visitors': 50000, 'conversions': 2500, 'rate': 0.05}
treatment = {'visitors': 50000, 'conversions': 2750, 'rate': 0.055}

# Z 检验（比例检验）
z_stat, p_value = stats.proportions_ztest(
    count=[treatment['conversions'], control['conversions']],
    nobs=[treatment['visitors'], control['visitors']]
)

# 置信区间
from statsmodels.stats.proportion import proportion_confint
ci_control = proportion_confint(control['conversions'], control['visitors'], alpha=0.05)
ci_treatment = proportion_confint(treatment['conversions'], treatment['visitors'], alpha=0.05)

# 提升率
effect_size = (treatment['rate'] - control['rate']) / control['rate']

print(f'=== A/B 测试结果 ===')
print(f'对照组: {control["rate"]:.3f} (95% CI: {ci_control[0]:.3f}-{ci_control[1]:.3f})')
print(f'实验组: {treatment["rate"]:.3f} (95% CI: {ci_treatment[0]:.3f}-{ci_treatment[1]:.3f})')
print(f'提升率: {effect_size:.1%}')
print(f'Z 统计量: {z_stat:.3f}')
print(f'p 值: {p_value:.4f}')
print(f'统计显著: {"是" if p_value < 0.05 else "否"}')

if p_value < 0.05 and effect_size > 0:
    print('\n结论: 实验版本显著优于对照组，建议发布')
else:
    print('\n结论: 未达到统计显著性，维持现状')
```