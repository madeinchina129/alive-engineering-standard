# Dio FAQ

## Q: Dio 和 http 包应该选哪个？

A: 项目中强制使用 Dio。http 包缺少拦截器、请求取消、自动重试等企业级特性。选择 Dio 而不是 http 包可以避免在每个项目中重复实现这些基础设施。

## Q: Dio 的拦截器执行顺序是什么？

A: 拦截器按照添加顺序组成调用链：
```
请求: 先添加的拦截器 → 后添加的拦截器 → HTTP 请求
响应: 后添加的拦截器 → 先添加的拦截器
```

推荐顺序：
```dart
dio.interceptors.addAll([
  AuthInterceptor,     // 1. 注入 token（最先处理请求，最后处理响应）
  LogInterceptor,      // 2. 日志记录
  RetryInterceptor,    // 3. 重试
  ErrorInterceptor,    // 4. 统一错误处理（最后处理请求，最先处理响应）
]);
```

## Q: 如何处理 Token 过期刷新？

A: 在 AuthInterceptor 中实现队列式刷新：

```dart
class AuthInterceptor extends Interceptor {
  bool _isRefreshing = false;
  final _pendingRequests = <({RequestOptions options, ErrorInterceptorHandler handler})>[];

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (err.response?.statusCode != 401) {
      return handler.next(err);
    }

    if (!_isRefreshing) {
      _isRefreshing = true;
      _refreshToken().then((_) {
        _isRefreshing = false;
        _retryPendingRequests();
      });
    }

    _pendingRequests.add((options: err.requestOptions, handler: handler));
  }
}
```

## Q: 如何配置多个不同 baseUrl 的 API？

A: 使用多个 Dio Provider：

```dart
final mainDioProvider = Provider<Dio>((ref) { /* baseUrl: api.example.com */ });
final authDioProvider = Provider<Dio>((ref) { /* baseUrl: auth.example.com */ });
final cdnDioProvider = Provider<Dio>((ref) { /* baseUrl: cdn.example.com */ });
```

## Q: 如何处理大文件上传进度？

```dart
final response = await dio.post(
  '/upload',
  data: FormData.fromMap({
    'file': await MultipartFile.fromFile(filePath),
  }),
  onSendProgress: (sent, total) {
    final progress = sent / total;
    ref.read(uploadProgressProvider.notifier).state = progress;
  },
);
```

## Q: Dio 如何处理 SSL Pinning？

```dart
(dio.httpClientAdapter as DefaultHttpClientAdapter).onHttpClientCreate =
    (client) {
  client.badCertificateCallback = (cert, host, port) {
    if (host == 'api.example.com') {
      return _verifyCertificate(cert); // 验证证书指纹
    }
    return false;
  };
};
```
