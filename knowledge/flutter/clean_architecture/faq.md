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
