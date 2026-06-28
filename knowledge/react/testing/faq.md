# React 测试 FAQ

## Q: `getBy`, `findBy`, `queryBy` 有什么区别？

```
getByText      → 元素存在则返回，不存在则抛错
findByText     → 返回 Promise，等待元素出现（默认 1000ms）
queryByText    → 元素存在则返回，不存在返回 null（不抛错）
```

```tsx
// 元素一定存在 → getBy
expect(screen.getByText('标题')).toBeInTheDocument()

// 异步出现 → findBy
expect(await screen.findByText('加载完成')).toBeInTheDocument()

// 测试元素不存在 → queryBy
expect(screen.queryByText('错误提示')).not.toBeInTheDocument()
```

## Q: 如何测试表单提交？

```tsx
test('form submission', async () => {
  const onSubmit = vi.fn()
  render(<Form onSubmit={onSubmit} />)
  const user = userEvent.setup()

  await user.type(screen.getByLabelText('用户名'), 'Alice')
  await user.type(screen.getByLabelText('密码'), '123456')
  await user.click(screen.getByRole('button', { name: '登录' }))

  expect(onSubmit).toHaveBeenCalledWith({ username: 'Alice', password: '123456' })
})
```

## Q: 如何测试组件中的路由跳转？

```tsx
import { MemoryRouter } from 'react-router-dom'

test('navigation', () => {
  render(
    <MemoryRouter initialEntries={['/']}>
      <App />
    </MemoryRouter>,
  )
  expect(screen.getByText('首页')).toBeInTheDocument()
})
```

## Q: `coverageThreshold` 设置多少合适？

```
statements: 80
branches: 75
functions: 80
lines: 80
```

建议核心业务模块 90%+，UI 组件可放宽到 70%。

## Q: Mock 全局变量怎么办？

```tsx
// Mock window.fetch
globalThis.fetch = vi.fn()

// Mock IntersectionObserver
const mockObserve = vi.fn()
globalThis.IntersectionObserver = vi.fn(() => ({ observe: mockObserve }))

// 记得 afterEach 清理
afterEach(() => { vi.restoreAllMocks() })
```

## Q: 如何测试 ErrorBoundary？

```tsx
test('error boundary catches error', () => {
  const ThrowError = () => { throw new Error('test error') }
  render(
    <ErrorBoundary fallback={<div>出错了</div>}>
      <ThrowError />
    </ErrorBoundary>,
  )
  // 注意：需要 console.error mock 避免测试输出污染
  expect(screen.getByText('出错了')).toBeInTheDocument()
})
```
