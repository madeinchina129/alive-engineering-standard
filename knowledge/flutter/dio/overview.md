# Dio 网络请求方案

## 为什么选择 Dio

### 功能完整

Dio 是 Flutter 生态最成熟的 HTTP 客户端，开箱即用：

```dart
final dio = Dio(BaseOptions(
  baseUrl: 'https://api.example.com',
  connectTimeout: const Duration(seconds: 10),
  receiveTimeout: const Duration(seconds: 10),
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
));
```

对比 http 包的原始使用，Dio 直接提供了企业级 HTTP 客户端所需的全部功能。

### 拦截器机制

Dio 的核心优势是拦截器链，可以在请求/响应生命周期的任意节点注入逻辑：

```dart
dio.interceptors.addAll([
  LogInterceptor(requestBody: true, responseBody: true),
  AuthInterceptor(),       // 自动 token 注入
  RetryInterceptor(),      // 自动重试
  CacheInterceptor(),      // 缓存控制
  ErrorInterceptor(),      // 统一错误处理
]);
```

对比 http 包需要手动为每个请求添加相同的逻辑。

### 自动序列化

```dart
// Dio + json_serializable 自动反序列化
final response = await dio.get('/users');
final users = (response.data as List)
    .map((e) => User.fromJson(e))
    .toList();
```

### 请求取消

```dart
final cancelToken = CancelToken();

// 发起请求
dio.get('/large-file', cancelToken: cancelToken);

// 取消请求（页面销毁时自动调用）
cancelToken.cancel('Request cancelled by user');
```

自动与 Riverpod 的 `ref.onDispose` 集成，页面销毁自动取消请求。

---

## 对比其他方案

| 维度 | http 包 | Dio |
|------|---------|-----|
| 拦截器 | 无 | ✅ 完整拦截器链 |
| 请求取消 | 手动 | ✅ CancelToken |
| 重试 | 无 | ✅ RetryInterceptor |
| 超时 | 手动 | ✅ 内置 connectTimeout/receiveTimeout |
| 表单数据 | 手动构建 | ✅ FormData 支持 |
| 文件上传 | MultipartRequest | ✅ 内置 |
| SSL Pinning | 无 | ✅ 支持 |
| 进度回调 | 无 | ✅ onSendProgress/onReceiveProgress |
| 适配器 | 无 | ✅ 可自定义 HttpClientAdapter |

---

## 适用范围

- **强制使用**：所有 HTTP API 请求
- **推荐使用**：文件上传下载、WebSocket（通过 WebSocketAdapter）
- **不建议**：gRPC（使用 gRPC-Dart）

## 与项目其他部分的集成

- **Riverpod**：Dio 实例通过 Provider 提供，拦截器通过 ref.onDispose 管理生命周期
- **GoRouter**：网络请求不受路由变化影响
- **Freezed**：响应数据反序列化为 Freezed 模型
