---
id: flutter.freezed
priority: P1
owner: Flutter Team
version: 1.0
generated: 2026-06-28
---

# Freezed 数据模型规范

> **领域**: Flutter 开发规范 | **优先级**: P1 | **版本**: 1.0
> 
> Flutter 不可变数据模型定义，序列化和 Union 类型标准


> **关联规范**: [Riverpod 状态管理规范](../10_Flutter/1023_Riverpod.md) · [Dio 网络请求规范](../10_Flutter/1025_Dio.md)


---




# Freezed 数据模型方案

## 为什么选择 Freezed

### 不可变数据模型

```dart
@freezed
class User with _$User {
  const factory User({
    required int id,
    required String name,
    required String email,
    @Default(UserStatus.active) UserStatus status,
  }) = _User;
  
  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```

自动生成：
- 不可变类（所有 field 为 final）
- `copyWith` 方法
- `==` 和 `hashCode`
- `toString`
- JSON 序列化/反序列化
- Union 类型（sealed class）

### 优势对比

```dart
// ❌ 手动编写
class User {
  final int id;
  final String name;
  // ... 手动实现 copyWith, ==, hashCode, toString, toJson, fromJson
}

// ✅ Freezed 生成
@freezed
class User with _$User {
  const factory User({required int id, required String name}) = _User;
  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```

### Union 类型支持

```dart
@freezed
sealed class ApiResult<T> with _$ApiResult<T> {
  const factory ApiResult.success(T data) = Success;
  const factory ApiResult.error(String message) = Error;
}

// 使用模式匹配
final result = apiResult.when(
  success: (data) => handleData(data),
  error: (message) => showError(message),
);
```

---

## 替代方案对比

| 维度 | 手写 | Freezed | equatable |
|------|------|---------|-----------|
| copyWith | 手动 | 自动 | 无 |
| ==/hashCode | 手动 | 自动 | 自动 |
| JSON | 手动 | 自动 | 无 |
| Union 类型 | 无 | 支持 | 无 |
| 代码量 | 多 | 最少 | 中 |
| 编译速度 | 快 | 较慢 | 快 |

---

## 适用范围

- **强制使用**：所有数据模型类
- **推荐使用**：API 响应 DTO、领域实体、事件
- **不适用**：Widget 状态类、Bloc 状态

## 与项目其他部分的集成

- **Riverpod**：Freezed 模型作为 Provider 的泛型参数
- **Dio**：响应数据反序列化为 Freezed 模型
- **GoRouter**：路由 extra 参数传递 Freezed 对象





---

## 使用规范

# Freezed 数据模型规范

## 模型定义规范

### 标准模型定义

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const factory User({
    required int id,
    required String name,
    required String email,
    @Default(UserStatus.active) UserStatus status,
    DateTime? lastLoginAt,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```

### 嵌套模型

```dart
@freezed
class Company with _$Company {
  const factory Company({
    required int id,
    required String name,
    required List<User> users,  // 嵌套自动处理
  }) = _Company;

  factory Company.fromJson(Map<String, dynamic> json) => _$CompanyFromJson(json);
}
```

## 强制规则 (MUST)

### 1. 所有 API 模型使用 Freezed

```dart
// ✅ 正确：所有数据模型使用 @freezed
@freezed
class LoginResponse with _$LoginResponse {
  const factory LoginResponse({
    required String token,
    required User user,
  }) = _LoginResponse;
  factory LoginResponse.fromJson(Map<String, dynamic> json) => _$LoginResponseFromJson(json);
}

// ❌ 禁止：手动编写数据模型
class LoginResponse {
  final String token;
  final User user;
  // 手动 copyWith, ==, hashCode, toString, toJson...
}
```

### 2. 使用 sealed class 表示有限状态

```dart
// ✅ 正确：sealed class 表示状态
@freezed
sealed class LoadState<T> with _$LoadState<T> {
  const factory LoadState.initial() = LoadInitial;
  const factory LoadState.loading() = LoadLoading;
  const factory LoadState.data(T data) = LoadData;
  const factory LoadState.error(String message) = LoadError;
}
```

### 3. 使用 @Default 提供默认值

```dart
@freezed
class Pagination with _$Pagination {
  const factory Pagination({
    @Default(1) int page,
    @Default(20) int pageSize,
    @Default(0) int total,
  }) = _Pagination;
  
  factory Pagination.fromJson(Map<String, dynamic> json) => _$PaginationFromJson(json);
}
```

### 4. 使用 Union 类型处理多返回值

```dart
// ✅ 正确：API 结果使用 union 类型
@freezed
sealed class ApiResult<T> with _$ApiResult<T> {
  const factory ApiResult.success(T data) = ApiSuccess<T>;
  const factory ApiResult.failure(ApiError error) = ApiFailure<T>;
}

// 使用 when 模式匹配
final result = await repository.fetchUser(id);
result.when(
  success: (user) => _handleUser(user),
  failure: (error) => _handleError(error),
);
```

### 5. 模型文件组织规范

```
lib/
├── models/
│   ├── user.dart          # User 模型
│   ├── user.freezed.dart  # 自动生成
│   ├── user.g.dart        # 自动生成
│   ├── company.dart       # Company 模型
│   ├── company.freezed.dart
│   ├── company.g.dart
│   ├── api_result.dart    # Union 类型
│   └── api_result.freezed.dart
```

## 推荐实践 (SHOULD)

### 1. 避免模型类过大（超过 10 个字段考虑拆分）

```dart
// ✅ 推荐：拆分为 User + Profile
@freezed
class User with _$User { /* 基础字段 */ }

@freezed
class UserProfile with _$UserProfile { /* 扩展字段 */ }
```

### 2. 使用 const constructor

```dart
const factory User({ ... }) = _User;  // ✅ const 构造函数
```

### 3. 生成文件添加到 .gitignore

```gitignore
*.freezed.dart
*.g.dart
```

## 禁止行为 (MUST NOT)

- ❌ 手动实现 copyWith、==、hashCode
- ❌ 在模型类中添加业务方法（仅在 domain 层使用）
- ❌ 使用 mutable 集合类型（使用 `List` 而非 `List?`）
- ❌ 在 Freezed 类中使用 `late` 关键字
- ❌ 编辑自动生成的 `.freezed.dart` 和 `.g.dart` 文件





---

## 代码示例

```dart
// Freezed 数据模型规范 — 示例
// Flutter 不可变数据模型定义，序列化和 Union 类型标准
// TODO: 补充具体实现
```





---

## 常见问题

# Freezed FAQ

## Q: Freezed 和 json_serializable 是什么关系？

A: Freezed 依赖于 json_serializable。`@freezed` 注解生成的 `.freezed.dart` 包含 copyWith/==/hashCode 等，而 `fromJson`/`toJson` 的序列化逻辑由 json_serializable 生成的 `.g.dart` 提供。

## Q: Freezed 生成的代码在哪里？是否应该提交？

A: 生成的文件在 `.freezed.dart` 和 `.g.dart` 中。建议添加到 `.gitignore`，在 CI/CD 中运行 `build_runner` 生成。但如果团队成员没有统一运行 build_runner 的习惯，可以提交生成文件。

## Q: Freezed 可以处理泛型吗？

```dart
@freezed
sealed class ApiResponse<T> with _$ApiResponse<T> {
  const factory ApiResponse.success(T data) = ApiSuccess<T>;
  const factory ApiResponse.failure(String message) = ApiFailure<T>;
  
  factory ApiResponse.fromJson(
    Map<String, dynamic> json,
    T Function(Object?) fromJsonT,
  ) => _$ApiResponseFromJson(json, fromJsonT);
}
```

## Q: copyWith 可以嵌套使用吗？

```dart
// Freezed 自动生成深层 copyWith
final updatedCompany = company.copyWith(
  address: company.address?.copyWith(city: 'New City'),
);
```

## Q: Freezed 和 Riverpod 如何配合？

```dart
@freezed
class UserState with _$UserState {
  const factory UserState({
    @Default([]) List<User> users,
    @Default(false) bool isLoading,
    String? error,
  }) = _UserState;
}

// 在 Notifier 中使用
class UserNotifier extends StateNotifier<UserState> {
  UserNotifier() : super(const UserState());
  
  Future<void> loadUsers() async {
    state = state.copyWith(isLoading: true);
    // ...
    state = state.copyWith(isLoading: false, users: users);
  }
}
```

## Q: @Freezed(copyWith: false) 什么时候用？

A: 当模型字段不应该被修改时（比如数据库 Entity），可以禁用 copyWith 以防止错误修改。





---

## 检查清单

# Freezed Code Review Checklist

## 模型定义
- [ ] 所有 API 数据模型是否使用 @freezed？
- [ ] 是否包含 `fromJson` 工厂方法？
- [ ] 是否使用 `@Default` 提供默认值？
- [ ] const factory 构造函数是否使用了命名参数？

## Union 类型
- [ ] 有限状态是否使用了 sealed class？
- [ ] Union 类型是否使用 when/map 模式匹配？
- [ ] 是否避免了 is 类型检查和强制转换？

## 序列化
- [ ] JSON 字段命名是否和 API 一致？（@JsonKey 处理不一致）
- [ ] 嵌套模型是否正确处理？
- [ ] 泛型模型的 fromJsonT 参数是否正确传递？

## 模型组织
- [ ] 模型文件是否集中在 models/ 目录？
- [ ] 大型模型是否拆分为更小的模型？
- [ ] 自动生成文件是否添加到 .gitignore？

## 代码质量
- [ ] 模型类中是否没有业务逻辑？
- [ ] 是否没有编辑自动生成的文件？
- [ ] 是否使用了 const 构造函数？
- [ ] 是否避免了 mutable 集合类型？





---

## AI Prompt

你是一个 Flutter 数据建模专家，精通 Freezed。请根据以下规范回答问题。

## 核心规范

### 模型定义
```dart
@freezed
class User with _$User {
  const factory User({
    required int id,
    required String name,
    @Default(UserStatus.active) UserStatus status,
  }) = _User;
  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```

### 强制规则
1. 所有 API 数据模型使用 @freezed，禁止手动编写
2. 使用 sealed class 表示有限状态
3. 使用 @Default 提供默认值
4. 使用 Union 类型处理多返回值
5. 避免模型类过大（超 10 字段考虑拆分）
6. 使用 const factory 构造函数

### 文件组织
- 模型集中在 models/ 目录
- 不编辑自动生成的 .freezed.dart / .g.dart 文件
- 生成文件建议 .gitignore

### 限制
- 模型类中不添加业务方法
- 避免使用 mutable 集合
- 避免使用 late 关键字

## 代码审查检查
审查时检查：@freezed 使用、fromJson 存在、@Default 默认值、sealed class 状态模型、copyWith 使用。




---

*本文档由 AES Knowledge Generator 自动生成。知识源：`knowledge/flutter/freezed/`*