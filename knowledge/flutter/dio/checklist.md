# Dio Code Review Checklist

## 实例管理
- [ ] Dio 是否通过 Provider 提供？（而非 `Dio()` 临时创建）
- [ ] 是否存在不必要的多个 Dio 实例？
- [ ] Provider 的 onDispose 中是否调用了 dio.close()？

## 请求封装
- [ ] API 调用是否封装在 Repository 中？
- [ ] UI 层是否没有直接使用 Dio？
- [ ] 每个请求是否都传递了 CancelToken？
- [ ] CancelToken 是否在 dispose 时 cancel？

## 拦截器
- [ ] AuthInterceptor 是否自动注入 Token？
- [ ] 401 响应是否正确处理了 Token 过期？
- [ ] ErrorInterceptor 是否覆盖了所有 DioExceptionType？
- [ ] handler.next/handler.resolve 是否正确调用？（没有漏调）

## 错误处理
- [ ] UI 层是否没有捕获 DioException？
- [ ] 超时、网络错误是否有用户友好的提示？
- [ ] 错误日志是否被正确记录？
- [ ] 是否区分了可重试和不可重试的错误？

## 安全
- [ ] 生产环境是否禁用了 LogInterceptor 的 requestBody？
- [ ] Token 是否存储在安全的位置？
- [ ] 是否没有在日志中打印敏感信息？

## 性能
- [ ] 页面退出时是否取消了正在进行的请求？
- [ ] 列表页面是否实现了请求去重？
- [ ] 图片/文件下载是否使用了 onReceiveProgress？
