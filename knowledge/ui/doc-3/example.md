```css
/* 响应式断点系统 */
:root {
  --bp-xs: 320px;
  --bp-sm: 576px;
  --bp-md: 768px;
  --bp-lg: 1024px;
}

/* 移动优先的栅格系统 */
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

@media (min-width: 576px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}

@media (min-width: 768px) {
  .grid { grid-template-columns: repeat(3, 1fr); }
}

@media (min-width: 1024px) {
  .grid { grid-template-columns: repeat(4, 1fr); }
}

/* 响应式导航 */
.nav {
  display: flex;
  gap: 24px;
}

@media (max-width: 767px) {
  .nav {
    display: none; /* 隐藏桌面导航 */
  }
  .hamburger {
    display: block; /* 显示汉堡菜单按钮 */
  }
  .nav.open {
    display: flex;
    flex-direction: column;
    position: absolute;
    top: 60px;
    left: 0;
    right: 0;
    background: white;
    padding: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  }
}
```