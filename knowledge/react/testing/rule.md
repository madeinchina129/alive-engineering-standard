# React 测试细则

## 强制规则 (MUST)

### 1. 查询优先使用 role 和 text

```tsx
// ✅ 正确：按角色和可见文本查询
test('renders button', () => {
  render(<Button label="提交" />)
  expect(screen.getByRole('button', { name: '提交' })).toBeInTheDocument()
})

// ❌ 错误：按 CSS 类名或 testid 查询（脆弱）
expect(document.querySelector('.btn-primary')).toBeInTheDocument()
```

### 2. 用户交互优先使用 userEvent

```tsx
// ✅ 正确：userEvent 模拟真实用户
import userEvent from '@testing-library/user-event'

test('input accepts text', async () => {
  const user = userEvent.setup()
  render(<Input />)
  const input = screen.getByRole('textbox')
  await user.type(input, 'hello')
  expect(input).toHaveValue('hello')
})

// ❌ 错误：fireEvent 不模拟真实行为链
fireEvent.change(input, { target: { value: 'hello' } })
```

### 3. 异步操作等待 UI 变化

```tsx
// ✅ 正确：waitFor / findBy
test('loads data', async () => {
  render(<UserList />)
  expect(await screen.findByText('Alice')).toBeInTheDocument()
})

// ❌ 错误：固定 timeout
setTimeout(() => {
  expect(screen.getByText('Alice')).toBeInTheDocument()
}, 1000)
```

### 4. 测试自定义 hooks 使用 renderHook

```tsx
// ✅ 正确：renderHook 测试 hooks
import { renderHook, act } from '@testing-library/react'

test('useCounter', () => {
  const { result } = renderHook(() => useCounter(0))
  act(() => result.current.increment())
  expect(result.current.count).toBe(1)
})

// ❌ 错误：在组件外直接调用 hooks
const { current } = useCounter(0)  // ❌ Invalid hook call
```

### 5. Mock API 使用 MSW

```tsx
// ✅ 正确：MSW 拦截请求
import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'

const server = setupServer(
  http.get('/api/users', () => HttpResponse.json([{ id: 1, name: 'Alice' }])),
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

## 推荐实践 (SHOULD)

### 按功能组织测试文件

```tsx
// components/UserCard/UserCard.test.tsx — 和组件同目录
// hooks/useUser.test.ts — 和 hooks 同目录
// __tests__/integration/login.test.tsx — 集成测试独立目录
```

## 禁止行为 (MUST NOT)

- ❌ 测试内部实现细节（state、props 名称）
- ❌ 使用 `data-testid` 作为首选查询
- ❌ 在测试中依赖定时器
- ❌ 共享可变测试数据
- ❌ 测试后不清理 mock
