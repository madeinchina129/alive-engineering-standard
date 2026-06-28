```css
/* 主题变量定义 */
:root,
[data-theme="light"] {
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F5F5F5;
  --color-bg-tertiary: #FAFAFA;
  --color-text-primary: #262626;
  --color-text-secondary: #8C8C8C;
  --color-border: #E8E8E8;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.06);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.08);
}

[data-theme="dark"] {
  --color-bg-primary: #121212;
  --color-bg-secondary: #1E1E1E;
  --color-bg-tertiary: #2A2A2A;
  --color-text-primary: #E8E8E8;
  --color-text-secondary: #A0A0A0;
  --color-border: #333333;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.4);
}
```