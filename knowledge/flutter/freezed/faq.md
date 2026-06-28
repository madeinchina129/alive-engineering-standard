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
