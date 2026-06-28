# Riverpod Code Review Checklist

## Provider 定义

- [ ] 每个 Provider 文件是否按 feature 组织？（禁止集中在一个文件）
- [ ] Provider 命名是否清晰表达了用途？（如 `userListProvider` 而非 `users`）
- [ ] 是否正确选择了 Provider 类型？（Provider / FutureProvider / NotifierProvider）
- [ ] 单例服务是否不用 autoDispose？（配置、日志、API 客户端）
- [ ] 页面级数据是否用了 autoDispose？（避免内存泄漏）
- [ ] 缓存场景是否显式使用了 keepAlive？

## Notifier / Controller

- [ ] Notifier 中是否没有直接调用 API？（应委托给 Repository）
- [ ] 异步操作是否正确处理了 loading / error / data 状态？
- [ ] 是否在 Notifier 中执行了副作用（导航、弹窗）？
- [ ] 状态更新是否是不可变的？（不要直接修改 state 的属性）
- [ ] `AsyncValue.guard` 是否替代了 try-catch 模板代码？

## Widget 层

- [ ] `ref.read` 是否只在事件回调中使用？（build 中禁止）
- [ ] `ref.watch` 是否在 build 中用于监听变化？
- [ ] Widget 是否只负责 UI 渲染？（业务逻辑在 Controller 中）
- [ ] `data.when` 是否完整处理了 data / loading / error 三种状态？
- [ ] 页面销毁时是否存在未清理的监听？

## 测试

- [ ] Controller 层是否有单元测试？
- [ ] 测试是否使用 `ProviderContainer(overrides: [...])` 而不是 Mockito？
- [ ] 是否测试了 error 状态下的 UI 表现？
- [ ] 异步操作是否测试了 loading / data 状态切换？

## 性能

- [ ] Provider 的依赖链是否过深？（超过 3 层应考虑合并）
- [ ] 是否存在不必要的重建？（ref.watch 的范围是否最小化）
- [ ] family 的参数是否稳定？（避免每次重建传入新对象）
- [ ] 是否存在循环依赖？（编译时会检测到）

## 常见违规示例

```dart
// ❌ 违规 1：build 中使用 ref.read
Widget build(BuildContext context, WidgetRef ref) {
  final user = ref.read(userProvider); // 应使用 ref.watch
}

// ❌ 违规 2：Widget 直接调用 API
Widget build(BuildContext context, WidgetRef ref) {
  final data = ref.watch(futureProvider); // API 调用隐藏在 Provider 中
}

// ❌ 违规 3：Notifier 中包含副作用
class BadController extends Notifier {
  void submit() {
    // 应返回结果，不应在这里导航
    Navigator.push(context, ...); // ❌
  }
}

// ✅ 正确做法
class GoodController extends Notifier<AsyncValue<SubmitResult>> {
  Future<void> submit() async {
    state = await AsyncValue.guard(() => repository.submit());
  }
  // Widget 层通过 ref.listen 处理导航
}
```

## 审查通过标准

- [ ] 所有 MUST 规则全部通过
- [ ] SHOULD 规则违规不超过 2 项
- [ ] 测试覆盖率 >= 80%
- [ ] 没有 lint 警告
- [ ] 性能影响已评估
