# Riverpod 使用规范

## Provider 类型选择

### 用哪种 Provider？

| 场景 | Provider 类型 | 说明 |
|------|--------------|------|
| 同步依赖注入 | `Provider` | 单例服务、配置 |
| 异步数据加载 | `FutureProvider` | API 请求、数据库查询 |
| 流式数据 | `StreamProvider` | WebSocket、实时数据 |
| 可变状态 | `NotifierProvider` | 复杂业务状态（推荐） |
| 简单可变状态 | `StateNotifierProvider` | 兼容旧代码 |
| 带参数查询 | `family` 修饰 | 列表项详情、分页 |

### 选择决策树

```
需要异步加载？
├── 是 → 数据会变化？
│   ├── 是 → StreamProvider
│   └── 否 → FutureProvider.autoDispose
└── 否 → 状态可变？
    ├── 是 → 逻辑复杂？
    │   ├── 是 → NotifierProvider
    │   └── 否 → StateProvider (仅简单场景)
    └── 否 → Provider
```

## 强制规则 (MUST)

### 1. 优先使用 Notifier 而非 StateNotifier

```dart
// ✅ 推荐：Notifier + NotifierProvider
class CounterNotifier extends Notifier<int> {
  @override
  int build() => 0;
  
  void increment() => state++;
}

final counterProvider = NotifierProvider<CounterNotifier, int>(
  CounterNotifier.new,
);

// ❌ 避免：StateNotifier（使用代码生成，依赖 freezed）
class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);
  
  void increment() => state++;
}
```

### 2. Provider 按 feature 组织

```dart
// ✅ 推荐：一个 feature 一个文件
// lib/feature/user/providers/user_providers.dart
final userApiProvider = Provider<UserApi>((ref) => UserApi(ref));
final userRepositoryProvider = Provider<UserRepository>((ref) {
  return UserRepository(ref.read(userApiProvider));
});
final userListProvider = FutureProvider.autoDispose<List<User>>((ref) {
  return ref.read(userRepositoryProvider).fetchAll();
});

// ❌ 禁止：所有 Provider 放在一个全局文件
// lib/providers/all_providers.dart ← 几千行，不可维护
```

### 3. Repository 只负责数据，Widget 只负责 UI

```dart
// ✅ 正确分层
final userRepositoryProvider = Provider<UserRepository>((ref) {
  return UserRepository(ref.read(apiProvider));
});

// Controller/ViewModel 层处理业务逻辑
final userListControllerProvider = Provider<UserListController>((ref) {
  return UserListController(ref.read(userRepositoryProvider));
});

// Widget 通过 Controller 获取数据
class UserListPage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final controller = ref.watch(userListControllerProvider);
    // Widget 只负责 UI 渲染
  }
}

// ❌ 错误：Widget 直接调用 API
class UserListPage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // ❌ Widget 不应该知道 API 的存在
    final response = ref.read(apiProvider).getUsers();
  }
}
```

### 4. 使用 autoDispose 避免内存泄漏

```dart
// ✅ 所有页面级 Provider 必须 autoDispose
final userDetailProvider = FutureProvider.autoDispose.family<User, String>(
  (ref, id) => ref.read(userRepositoryProvider).fetchById(id),
);

// ✅ 需要时用 keepAlive 保留缓存
final cachedDataProvider = FutureProvider.autoDispose<List<Data>>((ref) async {
  return ref.read(dataRepositoryProvider).fetchAll();
}).ref.keepAlive(); // 明确需要缓存时使用
```

### 5. ref.read 只能在回调中使用

```dart
// ✅ 正确：ref.read 在事件回调中使用
void onButtonPressed(WidgetRef ref) {
  ref.read(counterProvider.notifier).increment();
}

// ❌ 错误：ref.read 在 build 方法中使用
Widget build(BuildContext context, WidgetRef ref) {
  final value = ref.read(counterProvider); // ❌ build 中应该用 ref.watch
}

// ✅ 正确：build 中使用 ref.watch
Widget build(BuildContext context, WidgetRef ref) {
  final value = ref.watch(counterProvider);
}
```

### 6. 禁止在 Widget 中直接创建 HTTP 请求

```dart
// ❌ 禁止：Widget 直接调用 API
Widget build(BuildContext context, WidgetRef ref) {
  final data = ref.watch(futureProvider);
  return data.when(
    data: (data) => ...,
    error: (error, stack) => ...,
    loading: () => ...,
  );
}

// 原因：
// 1. Widget 不应该知道数据来源
// 2. 无法复用
// 3. 测试困难
```

## 推荐实践 (SHOULD)

### 1. 使用 family 处理参数化查询

```dart
final userDetailProvider = FutureProvider.autoDispose.family<User, String>(
  (ref, userId) => ref.read(userRepositoryProvider).fetchById(userId),
);

// 使用
final user = ref.watch(userDetailProvider(userId));
```

### 2. Provider 依赖通过 ref 传递

```dart
// ✅ 所有依赖通过 ref 获取
final userServiceProvider = Provider<UserService>((ref) {
  return UserService(
    api: ref.read(apiProvider),
    cache: ref.read(cacheProvider),
  );
});
```

### 3. 组合 Provider 而非继承

```dart
// ✅ 组合多个 Provider
final combinedDataProvider = FutureProvider<List<CombinedData>>((ref) async {
  final users = await ref.read(usersProvider.future);
  final orders = await ref.read(ordersProvider.future);
  return combine(users, orders);
});
```

## 禁止行为 (MUST NOT)

- ❌ 在 Provider 的 build 方法中执行副作用（导航、弹窗）
- ❌ 在 ref.listen 中调用 ref.read 修改同一个 Provider
- ❌ 在 Notifier 中直接调用 API（委托给 Repository）
- ❌ 使用全局变量作为状态替代 Riverpod
- ❌ 在 Widget build 中使用 `ref.read`（应使用 `ref.watch`）
- ❌ 创建循环依赖（Provider A 依赖 Provider B，B 又依赖 A）
