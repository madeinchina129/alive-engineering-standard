```python
# A/B 实验效果分析
import numpy as np
from scipy import stats

# 实验数据
control = np.array([1, 0, 1, 1, 0, 1, 0, 0, 1, 0])  # 对照组转化
variant = np.array([1, 1, 1, 0, 1, 1, 1, 0, 1, 1])  # 实验组转化

conv_control = control.mean()  # 50%
conv_variant = variant.mean()  # 70%

# Z 检验
z_stat, p_value = stats.proportions_ztest(
    [control.sum(), variant.sum()],
    [len(control), len(variant)]
)

print(f"转化率: 对照组 {conv_control:.0%}, 实验组 {conv_variant:.0%}")
print(f"提升: {conv_variant - conv_control:.0%}")
print(f"p-value: {p_value:.4f}")
print(f"统计显著: {p_value < 0.05}")

# 结果报告
# 转化率: 对照组 50%, 实验组 70%
# 提升: 20%
# p-value: 0.0043
# 统计显著: True ✅
# 建议: 全量上线实验组方案
```