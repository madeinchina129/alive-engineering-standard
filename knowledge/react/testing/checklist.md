# React 测试 Checklist

## 测试策略
- [ ] 是否遵循测试金字塔（单元 > 集成 > E2E）？
- [ ] 是否测试行为而非实现？
- [ ] 核心业务逻辑是否有 90%+ 覆盖率？
- [ ] UI 组件是否有 70%+ 覆盖率？

## 查询选择
- [ ] 是否优先使用 `getByRole` 和 `getByText`？
- [ ] 是否避免使用 `data-testid` 作为首选？
- [ ] 异步元素是否使用 `findBy` 而非固定 timeout？
- [ ] 测试不存在的元素是否使用 `queryBy`？

## 用户交互
- [ ] 用户交互是否使用 `userEvent` 而非 `fireEvent`？
- [ ] 表单测试是否模拟完整用户操作链？
- [ ] 是否使用了 `user.setup()` 创建实例？

## Mock
- [ ] API 是否使用 MSW 而非手动 mock fetch？
- [ ] mock 是否在 afterEach 中清理？
- [ ] hooks 是否使用 `renderHook` 测试？
- [ ] 是否避免 mock 内部实现？

## 异步测试
- [ ] 异步操作是否使用了 `await`？
- [ ] 是否使用了 `waitFor` 等待条件？
- [ ] 定时器是否使用 `vi.useFakeTimers()` 模拟？

## 测试组织
- [ ] 测试文件是否和源文件放在一起？
- [ ] 集成测试是否在 `__tests__` 目录？
- [ ] 测试是否有清晰的 describe/it 分层？
