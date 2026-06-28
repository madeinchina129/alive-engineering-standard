# Dio 网络请求规范

## 实例管理规则

### 单例 + Provider 模式

```dart
// ✅ 推荐：通过 Riverpod Provider 提供 Dio 实例
final dioProvider = Provider<Dio>((ref) {
  final dio = Dio(BaseOptions(
    baseUrl: AppConfig.apiBaseUrl,
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 10),
    headers: {'Content-Type': 'application/json'},
  ));

  dio.interceptors.addAll([
    AuthInterceptor(ref),
    LogInterceptor(requestBody: true, responseBody: true),
    ErrorInterceptor(ref),
  ]);

  ref.onDispose(dio.close);
  return dio;
});
```

### 共享还是独立实例

```dart
// ✅ 全局共享：默认情况下所有 API 使用同一 Dio 实例
// ❌ 仅当需要不同 baseUrl/超时配置时才创建独立实例
final authDioProvider = Provider<Dio>((ref) {
  return Dio(BaseOptions(
    baseUrl: 'https://auth.example.com',
    connectTimeout: const Duration(seconds: 5), // 认证接口短超时
  ));
});
```

## 强制规则 (MUST)

### 1. 统一错误处理

```dart
class ErrorInterceptor extends Interceptor {
  final Ref ref;

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    switch (err.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.receiveTimeout:
        _showSnackBar('网络连接超时，请稍后重试');
        break;
      case DioExceptionType.badResponse:
        _handleHttpError(err.response?.statusCode, err.response?.data);
        break;
      case DioExceptionType.cancel:
        // 用户取消，不处理
        break;
      default:
        _showSnackBar('网络请求失败，请检查网络连接');
    }
    handler.next(err); // 继续传递错误
  }
}
```

### 2. 使用 Repository 模式封装 API 调用

```dart
// ✅ 正确：Repository 封装 Dio 调用
class UserRepository {
  final Dio _dio;
  UserRepository(this._dio);

  Future<List<User>> fetchUsers() async {
    final response = await _dio.get('/users');
    return (response.data as List).map((e) => User.fromJson(e)).toList();
  }
}
```

```dart
// ✅ 正确：通过 Provider 提供 Repository
final userRepoProvider = Provider<UserRepository>((ref) {
  return UserRepository(ref.watch(dioProvider));
});
```

### 3. 所有请求携带 CancelToken

```dart
// ✅ 正确：每个请求都传递 CancelToken
class UserRepository {
  Future<List<User>> fetchUsers({CancelToken? cancelToken}) async {
    final response = await _dio.get('/users', cancelToken: cancelToken);
    return (response.data as List).map((e) => User.fromJson(e)).toJson();
  }
}
```

### 4. AuthInterceptor 自动注入 Token

```dart
class AuthInterceptor extends Interceptor {
  final Ref ref;

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    final token = ref.read(authTokenProvider);
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (err.response?.statusCode == 401) {
      ref.read(authProvider.notifier).logout();
      ref.read(routerProvider).go('/login');
      return;
    }
    handler.next(err);
  }
}
```

## 推荐实践 (SHOULD)

### 1. 日志拦截器按环境配置

```dart
if (kDebugMode) {
  dio.interceptors.add(LogInterceptor(
    requestBody: true,
    responseBody: true,
    logPrint: (o) => debugPrint('[DIO] $o'),
  ));
}
```

### 2. 重试策略

```dart
// 使用 retry 包或自定义 RetryInterceptor
// 重试幂等请求（GET），不重试写请求（POST/PUT/DELETE）
```

### 3. 使用枚举定义 API 端点

```dart
enum ApiEndpoint {
  login('POST', '/auth/login'),
  users('GET', '/users'),
  userDetail('GET', '/users/{id}'),
  updateUser('PUT', '/users/{id}');

  final String method;
  final String path;
  const ApiEndpoint(this.method, this.path);
}
```

## 禁止行为 (MUST NOT)

- ❌ 在 UI 层直接使用 Dio（必须通过 Repository）
- ❌ 不使用 CancelToken 发起请求
- ❌ 在拦截器中 catch 错误后不调用 handler 方法
- ❌ 在 UI 层 catch DioException 手动处理错误
- ❌ 在生产环境启用 LogInterceptor 打印请求体（包含敏感信息）
- ❌ 使用 `Dio().get(...)` 创建临时实例
