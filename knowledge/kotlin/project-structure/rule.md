# Kotlin 项目结构细则

## 强制规则 (MUST)

### 1. domain 层零框架依赖

```kotlin
// ✅ 正确：domain 层是纯 Kotlin
package com.example.domain.model

data class User(
    val id: Long,
    val name: String,
    val email: String,
)

// ❌ 错误：domain 依赖框架注解
data class User(
    @Id val id: Long,       // ❌ JPA 注解不应在 domain
    @Column val name: String,
)
```

### 2. 依赖方向：presentation → application → domain ← infrastructure

```kotlin
// ✅ 正确：application 引用 domain 接口
class CreateUserUseCase(
    private val userRepo: UserRepository,  // domain 接口，infra 实现
)

// ❌ 错误：application 直接引用 infrastructure 实现
class CreateUserUseCase(
    private val userRepo: JpaUserRepository,  // ❌ 耦合具体实现
)
```

### 3. data class 用于 DTO 和值对象

```kotlin
// ✅ 正确：DTO 用 data class
data class CreateUserRequest(
    val name: String,
    val email: String,
)

// ❌ 错误：DTO 用 class + boilerplate
class CreateUserRequest(
    val name: String,
    val email: String,
) // 缺少 copy()、componentN()、equals()、hashCode()
```

## 推荐实践 (SHOULD)

### 按 feature 分包（Android）

```
com.example.app/
├── feature/
│   ├── login/
│   │   ├── LoginScreen.kt
│   │   ├── LoginViewModel.kt
│   │   └── LoginRepository.kt
│   └── profile/
│       ├── ProfileScreen.kt
│       ├── ProfileViewModel.kt
│       └── ProfileRepository.kt
└── core/
    ├── network/
    └── database/
```

## 禁止行为 (MUST NOT)

- ❌ domain 层依赖 Spring/Android 框架
- ❌ 循环依赖（presentation → domain → presentation）
- ❌ 一个文件包含多个顶级类（data class 除外）
