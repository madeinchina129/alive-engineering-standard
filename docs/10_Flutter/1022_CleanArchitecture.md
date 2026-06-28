---
id: flutter.clean_architecture
priority: P0
owner: Flutter Team
version: 1.0
generated: 2026-06-28
---

# Clean Architecture 分层规范

> **领域**: Flutter 开发规范 | **优先级**: P0 | **版本**: 1.0
> 
> Flutter 项目分层架构标准，定义 Domain/Data/Presentation 层职责

> **关联规范**: [Riverpod 状态管理规范](../10_Flutter/1023_Riverpod.md)
[GoRouter 路由规范](../10_Flutter/1024_GoRouter.md)


---

---

# Clean Architecture 分层方案

## 为什么选择 Clean Architecture

### 三层架构

```
lib/
├── domain/           # 企业业务规则（纯 Dart，无框架依赖）
│   ├── models/       # 领域实体
│   ├── repositories/ # 仓库接口（抽象）
│   ├── usecases/     # 用例（业务逻辑编排）
│   └── enums/        # 领域枚举
├── data/             # 数据层实现
│   ├── datasources/  # 数据源（API、本地数据库）
│   ├── repositories/ # 仓库实现
│   └── models/       # DTO / 请求/响应模型
└── presentation/     # 表示层
    ├── providers/    # Riverpod Notifier
    ├── pages/        # 页面组件
    └── widgets/      # 可复用 Widget
```

### 依赖规则

```
presentation → domain ← data
                  ↑
              （依赖倒置）
```

- Domain 层不依赖任何外部框架
- Data 层实现 Domain 层定义的接口
- Presentation 层依赖 Domain 层

### 用例 (Use Case) 驱动

```dart
class GetUserProfile implements UseCase<UserProfile, int> {
  final UserRepository repository;
  
  GetUserProfile(this.repository);
  
  @override
  Future<Either<Failure, UserProfile>> call(int userId) {
    return repository.getProfile(userId);
  }
}
```

---

## 对比其他架构

| 维度 | Clean Architecture | MVC | 简单分层 |
|------|-------------------|-----|---------|
| 层数 | 3（domain/data/presentation） | 3（model/view/controller） | 2（ui/data） |
| 依赖方向 | domain 最内层 | 双向 | 单向 |
| 可测试性 | 最高（domain 纯 Dart） | 中 | 低 |
| 学习成本 | 高 | 低 | 最低 |
| 适用项目 | 中大型 | 小中型 | 原型/MVP |

---

## 适用范围

- **强制使用**：所有中大型 Flutter 项目
- **推荐**：MVP 阶段使用简化版，逐步演进
- **flexible**：Domain 层是必须的，Data/Presentation 可简化

## 与项目其他部分的集成

- **Riverpod**：Presentation 层通过 Provider 连接 UseCase 和 UI
- **Freezed**：Data 层的 DTO 和 Domain 层 Entity 使用 Freezed
- **Dio**：Data 层的远程数据源使用 Dio
- **GoRouter**：Presentation 层的路由配置


---

# Clean Architecture 分层规范

## 目录结构规范

### Domain 层

```dart
// domain/models/user.dart — 纯 Dart 实体（无框架依赖）
class User {
  final int id;
  final String name;
  final String email;
  final DateTime createdAt;
  
  const User({
    required this.id,
    required this.name,
    required this.email,
    required this.createdAt,
  });
}
```

```dart
// domain/repositories/user_repository.dart — 仓库接口
abstract class UserRepository {
  Future<Either<Failure, List<User>>> getUsers();
  Future<Either<Failure, User>> getUser(int id);
  Future<Either<Failure, User>> createUser(CreateUserParams params);
}
```

```dart
// domain/usecases/get_users.dart — 用例
class GetUsers {
  final UserRepository repository;
  
  GetUsers(this.repository);
  
  Future<Either<Failure, List<User>>> call() {
    return repository.getUsers();
  }
}
```

### Data 层

```dart
// data/datasources/user_remote_datasource.dart
class UserRemoteDataSource {
  final Dio dio;
  
  Future<List<UserDTO>> fetchUsers() async {
    final response = await dio.get('/users');
    return (response.data as List)
        .map((e) => UserDTO.fromJson(e))
        .toList();
  }
}
```

```dart
// data/repositories/user_repository_impl.dart
class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource remoteDataSource;
  
  @override
  Future<Either<Failure, List<User>>> getUsers() async {
    try {
      final dtos = await remoteDataSource.fetchUsers();
      return Right(dtos.map((dto) => dto.toDomain()).toList());
    } on DioException catch (e) {
      return Left(ServerFailure(e.message ?? 'Unknown error'));
    }
  }
}
```

### Presentation 层

```dart
// presentation/providers/user_provider.dart
final userListProvider = FutureProvider.autoDispose<List<User>>((ref) {
  final getUsers = ref.watch(getUsersProvider);
  return getUsers().then((either) => either.fold(
    (failure) => throw failure,
    (users) => users,
  ));
});
```

## 强制规则 (MUST)

### 1. Domain 层零依赖

```dart
// ✅ 正确：domain 层只导入 dart: 包
import 'package:fpdart/fpdart.dart'; // ✅ 纯函数式库

// ❌ 错误：domain 层导入 Flutter 或 Dio
import 'package:flutter/material.dart';   // ❌
import 'package:dio/dio.dart';            // ❌
```

### 2. 仓库接口在 Domain 层，实现在 Data 层

```dart
// domain/repositories/user_repository.dart — 接口
abstract class UserRepository {
  Future<Either<Failure, List<User>>> getUsers();
}

// data/repositories/user_repository_impl.dart — 实现
class UserRepositoryImpl implements UserRepository {
  // ...
}
```

### 3. Data 层 DTO 转 Domain Entity

```dart
// data/models/user_dto.dart
@freezed
class UserDTO with _$UserDTO {
  const factory UserDTO({
    required int id,
    required String name,
    required String email,
    required String createdAt,
  }) = _UserDTO;
  factory UserDTO.fromJson(Map<String, dynamic> json) => _$UserDTOFromJson(json);
}

extension UserDTOMapper on UserDTO {
  User toDomain() => User(
    id: id,
    name: name,
    email: email,
    createdAt: DateTime.parse(createdAt),
  );
}
```

### 4. UseCase 只做一件事

```dart
// ✅ 正确：每个 UseCase 一个方法
class GetUserProfile implements UseCase<UserProfile, int> { ... }
class UpdateUserProfile implements UseCase<UserProfile, UpdateParams> { ... }
class DeleteUserAccount implements UseCase<void, int> { ... }

// ❌ 错误：一个 UseCase 做多件事
class UserUseCase {
  Future<User> getProfile(int id) { ... }
  Future<User> updateProfile(UpdateParams p) { ... }
  Future<void> deleteAccount(int id) { ... }
}
```

### 5. 数据流方向: UI → Provider → UseCase → Repository → DataSource

```dart
// UI 点击事件
onPressed: () => ref.read(userListProvider.notifier).refresh();

// Provider 调用 UseCase
final getUsers = ref.read(getUsersProvider);
final result = await getUsers();

// UseCase 调用 Repository 接口
return repository.getUsers();

// RepositoryImpl 调用 DataSource
final dtos = await remoteDataSource.fetchUsers();
```

## 推荐实践 (SHOULD)

### 1. 使用 Either 处理错误

```dart
typedef FutureEither<T> = Future<Either<Failure, T>>;
```

### 2. 小项目简化规则

```dart
// 小项目可以直接 Provider → Repository，跳过 UseCase 层
// 但 Domain 和 Data 分离仍需保持
```

### 3. Entity 和 DTO 分离

```dart
// Entity: 业务关注的字段和类型
// DTO: API 返回的原始格式
// Mapper: 转换逻辑
```

## 禁止行为 (MUST NOT)

- ❌ Domain 层依赖任何框架
- ❌ Data 层直接返回 DTO 给 Presentation（必须转 Entity）
- ❌ Data 层抛出的异常直接传递到 UI 层
- ❌ Presentation 层直接调用 DataSource
- ❌ UseCase 之间相互依赖（应通过 Repository 共享数据）


---

# Clean Architecture FAQ

## Q: 小项目是否需要完整的 Clean Architecture？

A: 推荐保持 Domain/Data/Presentation 三层分离，但可以简化：
- **MVP 阶段**：跳过 UseCase 层，Provider 直接调用 Repository
- **小型项目**：保持三层目录结构，但 Entity 和 DTO 可合并
- **协作项目**：必须完整三层

## Q: Entity 和 DTO 的区别是什么？

| | Entity (Domain) | DTO (Data) |
|--|----------------|-------------|
| 依赖 | 纯 Dart | json_serializable / Freezed |
| 字段 | 业务关注的类型 | API 原始格式 |
| 示例 | `DateTime createdAt` | `String createdAt`（ISO 字符串）|
| 变更原因 | 业务需求变更 | API 格式变更 |

## Q: UseCase 到底有什么用？看起来只是转发。

```dart
// UseCase 的价值：
class GetUsers {
  final UserRepository repository;
  final AnalyticsService analytics;  // ✅ 在这里添加横切关注点
  
  Future<Either<Failure, List<User>>> call() async {
    analytics.log('get_users_started');  // 日志
    final result = await repository.getUsers();
    analytics.log('get_users_completed');  // 日志
    return result;
  }
}
```

UseCase 是横切关注点（日志、缓存、权限检查）的自然位置。

## Q: Either 和 try-catch 怎么选？

```dart
// ✅ 推荐：使用 Either 明确错误类型
Future<Either<Failure, User>> getProfile(int id);

// ✅ try-catch 仅用于不可恢复的错误
// ✅ Either 让调用方必须处理错误（编译期保证）
```

## Q: Repository 和 DataSource 的区别？

- **DataSource**：具体的数据获取方式（API、本地数据库、缓存）
- **Repository**：数据获取策略（先读缓存 → 失败走 API → 写入缓存）

```dart
class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource remote;
  final UserLocalDataSource local;
  
  Future<Either<Failure, List<User>>> getUsers() async {
    // 先读缓存
    final cached = await local.getCachedUsers();
    if (cached.isRight()) return cached;
    
    // 缓存失败，走 API
    final result = await remote.fetchUsers();
    result.fold(
      (l) => null,
      (users) => local.cacheUsers(users),  // 写入缓存
    );
    return result;
  }
}
```

## Q: 如何处理跨 UseCase 的通用逻辑？

A: 两种方式：
1. 提取到 Repository 层（推荐）
2. 使用组合而非继承

```dart
// ✅ 组合方式
class DeleteUser {
  final GetUserProfile getProfile;
  final UserRepository repository;
  
  Future<Either<Failure, void>> call(int id) async {
    final profile = await getProfile(id);
    return profile.fold(
      (failure) => Left(failure),
      (_) => repository.delete(id),
    );
  }
}
```


---

# Clean Architecture Code Review Checklist

## 目录结构
- [ ] 项目是否遵循 domain/data/presentation 三层结构？
- [ ] Domain 层是否零依赖？（没有 Flutter/Dio 导入）
- [ ] Data 层是否实现了 Domain 层的接口？
- [ ] Presentation 层是否只依赖 Domain 层？

## Domain 层
- [ ] Entity 是否纯 Dart 类？（无序列化注解）
- [ ] Repository 是否定义为抽象接口？
- [ ] UseCase 是否每个只做一件事？
- [ ] UseCase 命名是否清晰？（GetUsers, CreateUser, DeleteUser）
- [ ] 错误类型是否使用 Either/Failure 模式？

## Data 层
- [ ] DTO 是否转换为 Entity 后才返回？（不直接将 DTO 传到 UI）
- [ ] RepositoryImpl 是否正确处理了所有边缘情况？
- [ ] DataSource 是否只负责单一数据源？
- [ ] 缓存策略是否在 Repository 层实现？

## Presentation 层
- [ ] Provider 是否调用 UseCase 而非直接调用 Repository？
- [ ] UI 是否通过 Provider 访问状态？
- [ ] 是否没有在 Widget 中直接调用 DataSource？
- [ ] 错误是否在 Provider 层处理？

## 数据流
- [ ] 数据流方向是否正确：UI → Provider → UseCase → Repository → DataSource？
- [ ] 是否存在反向依赖？
- [ ] 依赖注入是否通过 Riverpod 实现？
- [ ] 是否避免了 UseCase 之间的直接依赖？

## 测试
- [ ] Domain 层是否可以纯单元测试？
- [ ] Repository 接口是否可以 mock？
- [ ] UseCase 是否可以独立测试？


---

你是一个 Flutter 架构专家，精通 Clean Architecture。请根据以下规范回答问题。

## 核心架构

### 三层结构
```
lib/
├── domain/          # 纯 Dart，无框架依赖
│   ├── models/      # 领域实体
│   ├── repositories/# 仓库抽象接口
│   └── usecases/    # 用例（每用例一文件一方法）
├── data/            # 实现
│   ├── datasources/ # API / 本地缓存
│   ├── repositories/# 仓库实现（DTO→Entity 转换）
│   └── models/      # DTO（序列化注解）
└── presentation/    # UI
    ├── providers/   # Riverpod Notifier
    ├── pages/       # 页面
    └── widgets/     # 组件
```

### 依赖规则
- Domain 不依赖任何外部框架
- Data 实现 Domain 接口
- Presentation 只依赖 Domain
- 数据流：UI → Provider → UseCase → Repository → DataSource

### 强制规则
1. Domain 层零框架依赖
2. Repository 接口在 Domain，实现在 Data
3. DTO 必须转 Entity 后才能向上传递
4. UseCase 只做一件事
5. 使用 Either<Failure, T> 处理错误
6. Data 层异常不直接传播到 UI

### 简化规则
- 小项目可跳过 UseCase 层，Provider 直接调 Repository
- 但 Domain/Data 分离必须保持

## 代码审查检查
审查时检查：三层目录结构、Domain 零依赖、DTO→Entity 转换、UseCase 单一职责、数据流方向。



---

*本文档由 AES Knowledge Generator 自动生成。知识源：`knowledge/flutter/clean_architecture/`*
