```tsx
// ✅ 好的组件设计：单一职责、类型完备
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'ghost' | 'danger';
  size: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  icon?: React.ReactNode;
  children: React.ReactNode;
  onClick?: () => void;
}

// ❌ 不好的组件设计：Props 过多、职责不单一
interface BadButtonProps {
  type: string;
  text: string;
  iconName?: string;
  iconPosition?: 'left' | 'right';
  loadingText?: string;
  confirmBeforeClick?: boolean;
  confirmMessage?: string;
  trackClick?: boolean;
  trackEventName?: string;
  // ...20+ more props
}
```