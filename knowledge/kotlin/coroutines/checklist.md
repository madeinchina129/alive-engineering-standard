# Kotlin 协程 Checklist

## Scope 管理
- [ ] 是否使用 `viewModelScope` / `lifecycleScope`？
- [ ] 是否避免 `GlobalScope`？
- [ ] 协程是否随组件生命周期自动取消？

## Dispatcher 选择
- [ ] 网络/IO 操作是否使用 `Dispatchers.IO`？
- [ ] CPU 计算是否使用 `Dispatchers.Default`？
- [ ] UI 更新是否在主线程？
- [ ] 是否避免在主线程执行阻塞操作？

## 异常处理
- [ ] launch 中是否有 try-catch？
- [ ] async 中异常是否被处理？
- [ ] 是否使用 `CoroutineExceptionHandler`？

## Flow
- [ ] 数据流是否使用 Flow 而非 Channel？
- [ ] IO 操作是否使用 `.flowOn(Dispatchers.IO)`？
- [ ] UI 层是否将 Flow 转为 LiveData/StateFlow？

## 并发
- [ ] 并行请求是否使用 `async`？
- [ ] 是否避免不必要的并发？
- [ ] 协程是否在合适时机取消？
