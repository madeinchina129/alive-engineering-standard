# React 测试规范

## 测试策略

### 测试金字塔

```
    ╱  E2E  ╲         少，覆盖关键用户流程
   ╱ Integration ╲     中，覆盖组件交互
  ╱   Unit Test   ╲   多，覆盖逻辑和 hooks
 ━━━━━━━━━━━━━━━━━━━
```

### 测试什么

```tsx
// ✅ 测试行为，而非实现
test('点击提交按钮后显示成功提示', async () => {
  render(<Form />)
  await userEvent.click(screen.getByRole('button', { name: '提交' }))
  expect(screen.getByText('提交成功')).toBeInTheDocument()
})

// ❌ 测试内部状态
test('提交按钮点击后 isLoading 为 true', () => {
  // 测试 React 内部状态是脆弱测试
})
```

---

## 测试工具选择

| 工具 | 用途 | 推荐度 |
|------|------|--------|
| Vitest | 测试运行器，快于 Jest | ⭐⭐⭐ |
| React Testing Library | 组件测试 | ⭐⭐⭐ |
| userEvent | 模拟用户交互 | ⭐⭐⭐ |
| MSW | API Mock | ⭐⭐⭐ |
| Playwright | E2E 测试 | ⭐⭐⭐ |

---

## 适用范围

- **单元测试**：所有 hooks、工具函数、纯组件
- **集成测试**：页面组件、表单提交、路由切换
- **E2E 测试**：核心用户流程（登录、注册、支付）
