import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

// ============================================
// Dio 实例 Provider
// ============================================

final dioProvider = Provider<Dio>((ref) {
  final dio = Dio(BaseOptions(
    baseUrl: 'https://api.example.com',
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 10),
    headers: {'Content-Type': 'application/json'},
  ));

  dio.interceptors.addAll([
    AuthInterceptor(ref),
    LogInterceptor(requestBody: true, responseBody: true),
    ErrorInterceptor(ref),
  ]);

  ref.onDispose(dio.close);
  return dio;
});

// ============================================
// 拦截器
// ============================================

class AuthInterceptor extends Interceptor {
  final Ref ref;
  AuthInterceptor(this.ref);

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    final token = ref.read(authTokenProvider);
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (err.response?.statusCode == 401) {
      ref.read(authProvider.notifier).logout();
      // 导航到登录页
      return;
    }
    handler.next(err);
  }
}

class ErrorInterceptor extends Interceptor {
  final Ref ref;
  ErrorInterceptor(this.ref);

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    switch (err.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.receiveTimeout:
        _showError('网络连接超时，请稍后重试');
      case DioExceptionType.badResponse:
        final statusCode = err.response?.statusCode;
        if (statusCode != null && statusCode >= 500) {
          _showError('服务器错误，请稍后重试');
        }
      default:
        _showError('网络请求失败，请检查网络连接');
    }
    handler.next(err);
  }

  void _showError(String message) {
    // 通过 ref 读取 SnackBar Provider 显示错误
  }
}

// ============================================
// 模型
// ============================================

class User {
  final int id;
  final String name;
  final String email;

  const User({required this.id, required this.name, required this.email});

  factory User.fromJson(Map<String, dynamic> json) => User(
        id: json['id'] as int,
        name: json['name'] as String,
        email: json['email'] as String,
      );
}

// ============================================
// Repository 层
// ============================================

class UserRepository {
  final Dio _dio;
  UserRepository(this._dio);

  Future<List<User>> fetchUsers({CancelToken? cancelToken}) async {
    final response = await _dio.get(
      '/users',
      cancelToken: cancelToken,
    );
    return (response.data as List)
        .map((e) => User.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<User> fetchUser(int id, {CancelToken? cancelToken}) async {
    final response = await _dio.get(
      '/users/$id',
      cancelToken: cancelToken,
    );
    return User.fromJson(response.data as Map<String, dynamic>);
  }

  Future<User> createUser({
    required String name,
    required String email,
    CancelToken? cancelToken,
  }) async {
    final response = await _dio.post(
      '/users',
      data: {'name': name, 'email': email},
      cancelToken: cancelToken,
    );
    return User.fromJson(response.data as Map<String, dynamic>);
  }
}

// ============================================
// Repository Provider
// ============================================

final userRepoProvider = Provider<UserRepository>((ref) {
  return UserRepository(ref.watch(dioProvider));
});

// ============================================
// Controller / Notifier
// ============================================

final userListProvider =
    AsyncNotifierProvider<UserListNotifier, List<User>>(UserListNotifier.new);

class UserListNotifier extends AsyncNotifier<List<User>> {
  CancelToken? _cancelToken;

  @override
  Future<List<User>> build() async {
    ref.onDispose(() => _cancelToken?.cancel());
    return _fetchUsers();
  }

  Future<List<User>> _fetchUsers() async {
    _cancelToken?.cancel();
    _cancelToken = CancelToken();

    final repo = ref.read(userRepoProvider);
    return repo.fetchUsers(cancelToken: _cancelToken);
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() => _fetchUsers());
  }
}

// ============================================
// UI 层
// ============================================

/*
// Widget 中使用
class UserListWidget extends ConsumerWidget {
  const UserListWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final usersAsync = ref.watch(userListProvider);

    return usersAsync.when(
      data: (users) => ListView.builder(
        itemCount: users.length,
        itemBuilder: (context, index) => ListTile(
          title: Text(users[index].name),
          subtitle: Text(users[index].email),
        ),
      ),
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (error, stack) => Center(child: Text('Error: $error')),
    );
  }
}
*/
