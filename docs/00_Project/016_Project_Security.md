# 安全策略

> 版本: v1.0 | 更新: 2026-06

## 概述

本文定义项目的安全策略和最佳实践，涵盖应用安全、数据安全、基础设施安全和应急响应流程。所有项目成员必须遵守本策略。

## 安全原则

```
1. 最小权限   — 每个角色/服务只拥有完成工作所需的最小权限
2. 纵深防御   — 多层安全防护，单层失效不影响整体安全
3. 默认安全   — 新系统的默认配置必须是安全的
4. 永不信任   — 对任何输入、任何请求做验证
5. 可审计     — 所有安全相关操作必须记录日志
```

## 应用安全

### 认证

| 要求 | 标准 |
|------|------|
| 密码策略 | 最少 10 位，含大小写+数字+特殊字符 |
| 密码存储 | bcrypt (cost >= 12) 或 Argon2id |
| MFA | 管理后台强制启用 |
| Session 管理 | JWT 过期时间 ≤ 30 分钟，Refresh Token ≤ 7 天 |
| 登录限流 | 同一 IP 5 次失败后锁定 15 分钟 |

### 授权

```java
// 正确的权限检查：方法级注解
@PreAuthorize("hasRole('ADMIN')")
@GetMapping("/admin/users")
public List<UserResponse> listAllUsers() {
    return userService.findAll();
}

// ❌ 错误：仅在 Controller 中判断（容易被绕过）
@GetMapping("/admin/users")
public List<UserResponse> listAllUsers(HttpServletRequest request) {
    if (!request.isUserInRole("ADMIN")) {
        throw new ForbiddenException();
    }
    return userService.findAll();
}
```

### 输入验证

```java
// 后端必须验证所有输入，前端验证仅用于体验
@Validated
public class CreateUserRequest {
    @NotBlank(message = "用户名不能为空")
    @Size(min = 3, max = 50, message = "用户名长度 3-50")
    @Pattern(regexp = "^[a-zA-Z0-9_]+$", message = "用户名只能包含字母数字和下划线")
    private String username;

    @Email(message = "邮箱格式不正确")
    private String email;
}
```

### SQL 注入防护

```java
// ✅ 正确：使用参数化查询
@Query("SELECT u FROM User u WHERE u.email = :email")
Optional<User> findByEmail(@Param("email") String email);

// ❌ 错误：字符串拼接 SQL
@Query("SELECT * FROM users WHERE email = '" + email + "'")
List<User> findByEmailUnsafe(String email);
```

## 数据安全

### 数据分类

| 分类 | 定义 | 示例 | 存储要求 |
|------|------|------|----------|
| 公开 | 无需保护 | 产品名称、公开 API | 无 |
| 内部 | 泄露有轻微影响 | 项目计划、内部文档 | 访问控制 |
| 敏感 | 泄露有重大影响 | 用户邮箱、手机号 | 加密存储 |
| 机密 | 泄露有致命影响 | 密码、支付信息、身份证号 | 加密 + 审计 |

### 加密要求

- 传输加密：TLS 1.3 (HTTPS)
- 静态加密：AES-256-GCM
- 密码哈希：bcrypt cost >= 12
- 密钥管理：使用 Vault / KMS，禁止硬编码

### 日志脱敏

```java
// ✅ 正确：敏感字段脱敏
log.info("User login: email={}", maskEmail(user.getEmail()));
// → User login: email=j***@example.com

// ❌ 错误：明文记录敏感信息
log.info("User login: email={}", user.getEmail());
```

## 基础设施安全

### 网络

- 所有服务部署在私有网络内
- 对外仅暴露 443 和 80 端口
- 数据库、Redis、MQ 仅内网访问
- 使用 WAF 防护 Web 应用

### 容器安全

```dockerfile
# 使用非 root 用户运行
FROM eclipse-temurin:21-jre
RUN useradd -m -u 1000 appuser
USER appuser
COPY --chown=appuser:appuser app.jar app.jar
CMD ["java", "-jar", "app.jar"]
```

### 密钥管理

```
禁止硬编码密钥的替代方案：
├── 开发环境：.env 文件（已 gitignore）
├── 测试环境：CI Secrets
├── 预发布/生产：Vault / AWS Secrets Manager / K8s Secrets
└── 本地开发：工具读取本地 credential 文件
```

## 安全开发生命周期 (SDL)

### 编码阶段

- 使用安全编码规范（本系列规范的各领域规则）
- IDE 安装安全插件（SonarLint、Snyk）

### 构建阶段

- 自动扫描依赖漏洞（mvn ossindex:audit）
- SAST 静态代码扫描（SonarQube）
- 镜像扫描（Trivy / Clair）

### 测试阶段

- DAST 动态安全测试
- 渗透测试（每季度）
- Fuzz 测试（对 API 输入）

### 发布阶段

- 安全 Checklist 必须全部通过
- 生产发布前进行安全评审（变更涉及敏感数据时）

## 应急响应

### 安全事件分级

| 级别 | 定义 | 响应时限 |
|------|------|----------|
| P0 | 数据泄露、服务中断 | 15 分钟 |
| P1 | 高危漏洞可被利用 | 2 小时 |
| P2 | 中危漏洞 | 24 小时 |
| P3 | 低危问题 | 7 天 |

### 应急流程

```
发现事件 → 上报安全组 → 评估级别 → 启动应急
              ↓                     ↓
          通知管理层             阻断攻击
              ↓                     ↓
          事后复盘 ← 恢复服务 ← 修复漏洞
```

### 必知联系方式

- 安全应急群：@security-oncall（企业微信 / Slack）
- 安全邮箱：security@company.com
- 上报时限：发现安全事件后 15 分钟内上报

## 相关文档

- [Spring Boot 安全控制](../12_SpringBoot/12_springboot_安全控制规范.md)
- [部署规范](../16_Deploy/16_deploy_部署规范.md)
- [合规规范](../24_Compliance/24_compliance_合规规范.md)
