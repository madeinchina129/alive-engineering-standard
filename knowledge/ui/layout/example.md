```css
/* 12 列栅格系统 */
.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* 页面结构层级 */
.page > .page-header { /* Level 1: 页面头部 */
  margin-bottom: 32px;
}
.page > .section { /* Level 1: 页面区域 */
  margin-bottom: 48px;
}
.section > .section-header {
  margin-bottom: 24px;
}
.section > .card { /* Level 2: 内容卡片 */
  padding: 24px;
  border-radius: 8px;
  background: white;
}

/* 间距令牌 */
:root {
  --space-4: 4px;
  --space-8: 8px;
  --space-12: 12px;
  --space-16: 16px;
  --space-24: 24px;
  --space-32: 32px;
  --space-48: 48px;
  --space-64: 64px;
}
```