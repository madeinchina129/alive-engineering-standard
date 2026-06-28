```typescript
// 数据看板组件示例：核心指标卡
import { Card, Trend, Sparkline } from '@ant-design/charts';

interface MetricCardProps {
  title: string;
  value: number;
  unit: string;
  trend: 'up' | 'down' | 'flat';
  changePercent: number;
  sparklineData: number[];
  baseline: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title, value, unit, trend, changePercent, sparklineData, baseline
}) => {
  const colorMap = { up: '#52c41a', down: '#ff4d4f', flat: '#faad14' };
  
  return (
    <Card className="metric-card" hoverable>
      <div className="metric-title">{title}</div>
      <div className="metric-value" style={{ color: colorMap[trend] }}>
        {value.toLocaleString()}<span className="metric-unit">{unit}</span>
      </div>
      <div className="metric-trend">
        <Trend type={trend} />
        <span className="change" style={{ color: colorMap[trend] }}>
          {changePercent > 0 ? '+' : ''}{changePercent}%
        </span>
        <span className="baseline">vs {baseline}</span>
      </div>
      <Sparkline data={sparklineData} height={40} width={200} />
    </Card>
  );
};
```