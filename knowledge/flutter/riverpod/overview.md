# Riverpod 状态管理方案

## 为什么选择 Riverpod

### 编译安全

Riverpod 最核心的优势是**编译安全**。Provider 不存在时编译直接报错，而不是在运行时抛 `ProviderNotFoundException`。这意味着：

- 重构时删除一个 Provider，所有引用它的地方立即编译报错
- 新增 Provider 只需要在定义处声明，无需在 Widget Tree 某个祖先节点注册
- 永远不会出现"运行时找不到 Provider"的 crash

对比 Provider 方案：
```dart
// Provider 方案：运行时可能 crash
final user = Provider.of<UserProvider>(context); // ❌ 如果 ancestor 没有 provide 就 crash

// Riverpod 方案：编译时保证
final user = ref.watch(userProvider); // ✅ 不存在时编译直接报错
```

### 无 BuildContext 依赖

Riverpod 的 Provider 不依赖 Widget Tree，这意味着：

- **Service 层可以直接使用 Provider** — 不需要把 context 传到 Repository
- **测试时可以独立 override** — 不需要包裹 WidgetTree
- **Provider 可以在 initState 之前使用** — 没有生命周期限制

```dart
// Provider 方案：Service 层无法使用
class UserRepository {
  // 需要 context -> 但 Service 层不应该有 context
  final userProvider = Provider.of<UserProvider>(context);
}

// Riverpod 方案：Service 层原生支持
class UserRepository {
  final Ref ref;
  UserRepository(this.ref);
  
  Future<User> fetchUser() async {
    final api = ref.read(apiProvider);
    return api.getUser();
  }
}
```

### 自动销毁

Riverpod 的 `autoDispose` 修饰符会在 Provider 不再被监听时自动释放资源：

```dart
// 页面销毁时自动取消网络请求、关闭数据库连接
final userListProvider = FutureProvider.autoDispose<List<User>>((ref) async {
  final api = ref.read(apiProvider);
  return api.fetchUsers();
});
```

对比 Provider 方案需要手动 `dispose()`，忘记调用会导致内存泄漏。

### 可测试性

Riverpod 的 override 机制让测试变得极其简单：

```dart
// 测试时覆盖任何 Provider
final diProvider = Provider<String>((ref) => "production");

void main() {
  test("override example", () {
    final container = ProviderContainer(overrides: [
      diProvider.overrideWithValue("test"),
    ]);
    expect(container.read(diProvider), "test");
  });
}
```

不需要 Mockito，不需要创建复杂的测试 Widget 树。

---

## 与 Provider 的详细对比

| 维度 | Provider | Riverpod |
|------|----------|----------|
| 编译安全 | ❌ 运行时抛异常 | ✅ 编译时报错 |
| 依赖 Widget Tree | ✅ 必须 | ❌ 不需要 |
| Service 层可用 | ❌ | ✅ |
| 自动 dispose | ❌ 手动 | ✅ autoDispose |
| 测试覆盖 | ❌ 需要 Widget 树 | ✅ ProviderContainer |
| 多实例 | ❌ 不支持 | ✅ family |
| 代码生成 | ❌ | ✅ Riverpod Generator |
| 异步支持 | ❌ | ✅ FutureProvider + StreamProvider |

---

## 适用范围

- **强制使用**：所有涉及状态共享的场景
- **推荐使用**：API 请求、缓存、本地数据
- **不建议**：纯 UI 状态（用 StatefulWidget 或 useState）

## 与项目其他部分的集成

- **Dio**：通过 Provider 提供 Dio 实例，拦截器通过 Riverpod 的 ref.onDispose 管理生命周期
- **GoRouter**：在 Provider 中监听路由变化，通过 ref.listen 实现导航响应
- **Freezed**：与 Riverpod 的 StateNotifier 配合，实现不可变状态管理
- **Clean Architecture**：Riverpod 作为依赖注入容器，连接各层
