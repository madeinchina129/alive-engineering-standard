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
