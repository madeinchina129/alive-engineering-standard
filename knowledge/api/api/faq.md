# API 安全规范 — FAQ

## Q1: JWT Token 应该存在哪里？
Web 端使用 httpOnly Cookie（防 XSS 窃取），移动端使用安全存储（iOS Keychain / Android EncryptedSharedPreferences）。不要使用 localStorage（易受 XSS 攻击）。

## Q2: 如何防止 API 被恶意调用？
① IP 级别和用户级别的双维度限流 ② 查接口频次异常告警 ③ CAPTCHA 验证 ④ API 签名校验（如 HMAC）⑤ 敏感操作需二次确认。

## Q3: CORS 配置有什么注意的？
不要使用 Access-Control-Allow-Origin: *。明确指定允许的域名来源。不要在响应中暴露认证相关的 Header。不要在 OPTIONS 预检请求中泄露敏感信息。
