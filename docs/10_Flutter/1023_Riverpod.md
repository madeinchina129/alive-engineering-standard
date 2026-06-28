---
id: flutter.riverpod
priority: P0
owner: Flutter Team
version: 1.0
generated: 2026-06-28
---

# Riverpod 状态管理规范

> **领域**: Flutter 开发规范 | **优先级**: P0 | **版本**: 1.0
> 
> Flutter 统一状态管理方案，定义 Provider 选择、分层架构、测试策略

> **关联规范**: [Dio 网络请求规范](../10_Flutter/1025_Dio.md)
[Freezed 数据模型规范](../10_Flutter/1026_Freezed.md)
[GoRouter 路由规范](../10_Flutter/1024_GoRouter.md)
[Clean Architecture 分层规范](../10_Flutter/1022_CleanArchitecture.md)


---

---

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


---

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


---

// ignore_for_file: avoid_print
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';

// =============================================================================
// 1. 基础 API Provider
// =============================================================================

final dioProvider = Provider<Dio>((ref) {
  final dio = Dio(BaseOptions(
    baseUrl: 'https://api.example.com',
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 10),
  ));
  dio.interceptors.add(LogInterceptor(responseBody: true));
  ref.onDispose(() => dio.close());
  return dio;
});

// =============================================================================
// 2. 数据模型 (使用 Freezed 生成)
// =============================================================================

// user.dart — 实际项目中由 freezed 生成
class User {
  final String id;
  final String name;
  final String email;

  const User({
    required this.id,
    required this.name,
    required this.email,
  });

  factory User.fromJson(Map<String, dynamic> json) => User(
        id: json['id'] as String,
        name: json['name'] as String,
        email: json['email'] as String,
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'name': name,
        'email': email,
      };
}

// =============================================================================
// 3. Repository 层
// =============================================================================

class UserRepository {
  final Dio _dio;

  UserRepository(this._dio);

  Future<List<User>> fetchUsers() async {
    final response = await _dio.get('/users');
    return (response.data as List).map((e) => User.fromJson(e)).toList();
  }

  Future<User> fetchUserById(String id) async {
    final response = await _dio.get('/users/$id');
    return User.fromJson(response.data);
  }

  Future<User> createUser({required String name, required String email}) async {
    final response = await _dio.post('/users', data: {
      'name': name,
      'email': email,
    });
    return User.fromJson(response.data);
  }
}

final userRepositoryProvider = Provider<UserRepository>((ref) {
  return UserRepository(ref.read(dioProvider));
});

// =============================================================================
// 4. Controller / ViewModel 层
// =============================================================================

class UserListController extends Notifier<AsyncValue<List<User>>> {
  @override
  AsyncValue<List<User>> build() => const AsyncValue.loading();

  Future<void> loadUsers() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() => ref.read(userRepositoryProvider).fetchUsers());
  }

  Future<void> addUser(String name, String email) async {
    final repo = ref.read(userRepositoryProvider);
    await repo.createUser(name: name, email: email);
    await loadUsers(); // 刷新列表
  }
}

final userListControllerProvider =
    NotifierProvider<UserListController, AsyncValue<List<User>>>(
  UserListController.new,
);

// =============================================================================
// 5. Widget 层
// =============================================================================

// 页面入口
class UserListPage extends ConsumerWidget {
  const UserListPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final usersAsync = ref.watch(userListControllerProvider);

    ref.listen(userListControllerProvider, (prev, next) {
      next.whenOrNull(
        error: (err, stack) {
          // 全局错误处理
          print('Error loading users: $err');
        },
      );
    });

    return Scaffold(
      appBar: AppBar(title: const Text('Users')),
      body: usersAsync.when(
        data: (users) => ListView.builder(
          itemCount: users.length,
          itemBuilder: (context, index) => ListTile(
            title: Text(users[index].name),
            subtitle: Text(users[index].email),
          ),
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('Error: $error'),
              ElevatedButton(
                onPressed: () =>
                    ref.read(userListControllerProvider.notifier).loadUsers(),
                child: const Text('Retry'),
              ),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _showAddUserDialog(context, ref),
        child: const Icon(Icons.add),
      ),
    );
  }

  void _showAddUserDialog(BuildContext context, WidgetRef ref) {
    // 仅示例，实际应提取为独立的 Dialog Widget
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Add User'),
        content: const Text('Dialog implementation'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Cancel'),
          ),
        ],
      ),
    );
  }
}

// =============================================================================
// 6. 带参数查询 (family)
// =============================================================================

final userDetailProvider =
    FutureProvider.autoDispose.family<User, String>((ref, userId) async {
  final repo = ref.read(userRepositoryProvider);
  return repo.fetchUserById(userId);
});

class UserDetailPage extends ConsumerWidget {
  final String userId;
  const UserDetailPage({super.key, required this.userId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsync = ref.watch(userDetailProvider(userId));
    return Scaffold(
      appBar: AppBar(title: const Text('User Detail')),
      body: userAsync.when(
        data: (user) => Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Name: ${user.name}', style: const TextStyle(fontSize: 18)),
              const SizedBox(height: 8),
              Text('Email: ${user.email}'),
            ],
          ),
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, _) => Center(child: Text('Error: $error')),
      ),
    );
  }
}


---

# Riverpod FAQ

## Q: Notifier 和 StateNotifier 有什么区别？应该用哪个？

**A:** `Notifier` 是 Riverpod 2.x 引入的替代方案，推荐在新代码中使用。

| 维度 | StateNotifier | Notifier |
|------|---------------|----------|
| 代码量 | 需要定义 State 类 + Notifier 类 | 只需要 Notifier 类 |
| 不可变状态 | 依赖 freezed 或手动 copyWith | 同理 |
| 内置功能 | 基础 | 更多生命周期回调 |
| 社区趋势 | 维护模式 | 推荐方案 |

**结论**：新代码使用 `Notifier` + `NotifierProvider`。仅在维护旧代码时使用 `StateNotifier`。

## Q: ref.read 和 ref.watch 有什么区别？

**A:** 这是 Riverpod 中最常被误解的概念。

- `ref.watch(provider)` — 监听变化，当 provider 的值变化时，当前 widget/provider 会重建
- `ref.read(provider)` — 读取当前值，不监听变化

**规则**：
- `build` 方法中：使用 `ref.watch`
- 事件回调中：使用 `ref.read`
- `ref.read` 在 build 中使用会导致 lint 警告

## Q: autoDispose 和 keepAlive 怎么配合使用？

**A:** `autoDispose` 让 provider 在不再被监听时自动销毁，`keepAlive` 阻止自动销毁。

```dart
// 页面级数据：autoDispose
final pageDataProvider = FutureProvider.autoDispose<List<Data>>((ref) async {
  return fetchData();
});

// 需要缓存的全局数据：autoDispose + keepAlive
final cacheProvider = FutureProvider.autoDispose<List<Data>>((ref) async {
  return fetchExpensiveData();
}).ref.keepAlive(); // 即使没有监听也保留

// 手动控制缓存失效
final cacheProvider2 = FutureProvider.autoDispose<List<Data>>((ref) async {
  final link = ref.keepAlive();
  ref.onDispose(() => link.close());
  return fetchData();
});
```

**最佳实践**：
- 页面/组件级数据：只用 `autoDispose`
- 全局配置/缓存：`autoDispose` + `keepAlive`
- 服务单例：不用 `autoDispose`

## Q: 如何测试 Riverpod 代码？

**A:** 使用 `ProviderContainer`，无需 Flutter Widget 测试框架。

```dart
void main() {
  test('UserListController loads users', () async {
    // 创建测试容器，覆盖真实 API
    final container = ProviderContainer(overrides: [
      userRepositoryProvider.overrideWithValue(
        MockUserRepository(), // 返回测试数据
      ),
    ]);

    // 触发加载
    await container.read(userListControllerProvider.notifier).loadUsers();

    // 验证状态
    final state = container.read(userListControllerProvider);
    expect(state.valueOrNull?.length, greaterThan(0));
  });
}
```

## Q: Riverpod 如何处理依赖循环？

**A:** 循环依赖在编译时就能发现（Riverpod 会检测并抛出 `ProviderException`）。

解决方案：
1. **拆分 Provider**：将循环中的公共逻辑提取为独立 Provider
2. **延迟加载**：使用 `ref.read` 而非 `ref.watch` 打破循环
3. **重新设计**：循环依赖通常意味着设计问题，考虑重新划分职责

```dart
// ❌ 循环依赖：A 依赖 B，B 依赖 A
final aProvider = Provider((ref) => A(ref.read(bProvider)));
final bProvider = Provider((ref) => B(ref.read(aProvider)));

// ✅ 解决方案：提取公共依赖 C
final cProvider = Provider((ref) => C());
final aProvider = Provider((ref) => A(ref.read(cProvider)));
final bProvider = Provider((ref) => B(ref.read(cProvider)));
```

## Q: family 修饰符怎么用？有什么限制？

**A:** `family` 让 Provider 接受参数，每个参数值对应独立的 Provider 实例。

```dart
// 定义
final userProvider = FutureProvider.autoDispose.family<User, String>(
  (ref, userId) => fetchUser(userId),
);

// 使用
final user = ref.watch(userProvider('user-123'));
final user2 = ref.watch(userProvider('user-456')); // 独立实例
```

**限制**：
- 参数必须实现 `hashCode` 和 `==`
- 参数数量过多时考虑封装为对象
- 每次参数变化都会创建新的 Provider 实例

## Q: Provider 中如何访问路由参数？

**A:** 通过 GoRouter + Riverpod 集成。

```dart
// 方案 1：在页面组件中读取路由参数，传给 Provider
final userProvider = FutureProvider.autoDispose.family<User, String>(
  (ref, userId) => ref.read(userRepositoryProvider).fetchById(userId),
);

class UserPage extends ConsumerWidget {
  const UserPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userId = GoRouterState.of(context).pathParameters['id']!;
    final userAsync = ref.watch(userProvider(userId));
    // ...
  }
}

// 方案 2：通过 Provider 封装路由参数读取
final currentUserIdProvider = Provider<String?>((ref) {
  final routeState = ref.watch(goRouterProvider);
  return routeState.pathParameters['id'];
});
```

## Q: Notifier 中如何调用异步操作？

**A:** `Notifier` 的 `state` 是同步的，异步操作需要配合 `AsyncValue`。

```dart
class UserController extends Notifier<AsyncValue<List<User>>> {
  @override
  AsyncValue<List<User>> build() => const AsyncValue.loading();

  Future<void> loadUsers() async {
    state = const AsyncValue.loading();
    try {
      final users = await ref.read(userRepositoryProvider).fetchUsers();
      state = AsyncValue.data(users);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }
}
```

或者使用 `AsyncValue.guard` 简化：

```dart
state = await AsyncValue.guard(
  () => ref.read(userRepositoryProvider).fetchUsers(),
);
```

## Q: Provider 的 ref 和 WidgetRef 有什么区别？

**A:** 本质相同，但使用场景不同：

- `Ref` — 在 Provider 的 build 方法中使用
- `WidgetRef` — 在 ConsumerWidget 中使用

在 Provider 中获取另一个 Provider：
```dart
final myProvider = Provider((ref) {
  final other = ref.watch(otherProvider); // ✅ Ref
});
```

在 Widget 中获取 Provider：
```dart
Widget build(BuildContext context, WidgetRef ref) {
  final my = ref.watch(myProvider); // ✅ WidgetRef
}
```

两者都支持 `watch`, `read`, `listen`, `invalidate` 等方法。


---

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


---

你是一个 Flutter 状态管理专家，精通 Riverpod。请根据以下规范回答用户的问题。

## 你的角色

- 你正在参与一个使用 Flutter + Riverpod 的企业级项目
- 团队遵循严格的 Riverpod 使用规范
- 你需要确保你的建议符合团队规范

## 核心规范

### Provider 选择规则

| 场景 | Provider 类型 |
|------|--------------|
| 同步依赖注入 | `Provider` |
| 异步数据加载 | `FutureProvider.autoDispose` |
| 流式数据 | `StreamProvider` |
| 复杂可变状态 | `NotifierProvider` + `Notifier` |

### 强制规则

1. **Notifier 优先于 StateNotifier** — 新代码使用 `Notifier` + `NotifierProvider`
2. **Provider 按 feature 组织** — 每个 feature 一个文件，禁止全局 provider 文件
3. **Repository 只负责数据，Widget 只负责 UI** — Controller 层处理业务逻辑
4. **autoDispose 默认启用** — 页面级 Provider 必须 autoDispose，缓存场景显式 keepAlive
5. **ref.read 仅在回调中使用** — build 中使用 ref.watch
6. **禁止 Widget 直接调用 API** — API 调用封装在 Repository 中

### 代码生成要求

当你提供代码示例时：

1. 使用 Riverpod 2.x 语法（`Notifier`, `AsyncValue.guard`）
2. 包含完整的 Provider 链（API → Repository → Controller → Widget）
3. 正确处理 loading / error / data 三种状态
4. 使用 `ref.onDispose` 管理资源清理
5. 测试代码使用 `ProviderContainer(overrides: [...])` 而非 Mockito

### 代码审查要求

审查代码时，检查以下问题：

1. Provider 类型选择是否合理？
2. autoDispose 使用是否正确？
3. 是否存在 Widget 直接调用 API 的情况？
4. build 方法中是否误用了 ref.read？
5. 异步操作是否处理了所有状态？
6. 是否存在循环依赖？
7. 测试覆盖是否充分？

## 输出格式

### 回答问题

- 简短问题：给出结论 + 代码示例
- 复杂问题：先分析问题，再给出方案，最后提供代码
- 审查请求：按优先级列出问题，每个问题附上修改建议

### 代码示例

```dart
// 包含完整上下文，可运行的代码片段
```

### 禁用行为

- ❌ 不要推荐已经废弃的 Riverpod 0.x API
- ❌ 不要使用 ChangeNotifier + Provider 的混搭模式
- ❌ 不要在 Provider 中直接创建数据库连接（应通过 Repository）
- ❌ 不要推荐全局单例模式替代 Riverpod

## 项目上下文

- 项目使用 Flutter 3.x + Dart 3.x
- Riverpod 版本：2.x
- 网络层：Dio
- 路由：GoRouter
- 序列化：Freezed + json_serializable
- 测试：flutter_test + ProviderContainer

请根据以上规范回答用户的下一个问题。



---

*本文档由 AES Knowledge Generator 自动生成。知识源：`knowledge/flutter/riverpod/`*
