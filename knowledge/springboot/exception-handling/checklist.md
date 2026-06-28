# 统一异常处理 Code Review Checklist

## 异常类定义
- [ ] 是否有自定义业务异常基类？（BusinessException）
- [ ] 业务异常是否继承 BusinessException？
- [ ] 异常是否包含错误码？
- [ ] 是否定义了完善的 ErrorCode 枚举？

## 全局处理器
- [ ] 是否使用 @RestControllerAdvice？
- [ ] 是否覆盖了常见异常类型？（NotFound/Validation/Auth/Permission/General）
- [ ] 是否区分了业务异常和系统异常的日志级别？（warn vs error）
- [ ] 系统异常是否不暴露堆栈信息？
- [ ] 参数校验异常是否返回字段级错误详情？

## Service 层
- [ ] 业务异常是否在 Service 层抛出？
- [ ] 是否使用 Optional.orElseThrow 而非 if-null-check？
- [ ] 是否避免在 Service 层 catch 后吞掉异常？

## Controller 层
- [ ] Controller 是否没有 try-catch 业务异常？
- [ ] Controller 是否没有手动构建错误响应？
- [ ] 是否使用了 @Valid/@Validated 进行参数校验？

## 安全
- [ ] 500 错误是否不暴露内部细节？
- [ ] 错误日志是否包含请求追踪 ID？
- [ ] 是否记录完整堆栈用于排错？
- [ ] 敏感业务是否有审计日志？

## 边界情况
- [ ] Feign/RestTemplate 调用异常是否处理？
- [ ] 异步方法异常是否处理？
- [ ] 文件上传异常是否处理？
- [ ] 类型转换异常是否处理？
