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
