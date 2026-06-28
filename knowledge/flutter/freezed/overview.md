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
