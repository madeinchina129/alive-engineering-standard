// ignore_for_file: avoid_print
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';

// =============================================================================
// 1. 基础 API Provider
// =============================================================================

final dioProvider = Provider<Dio>((ref) {
  final dio = Dio(BaseOptions(
    baseUrl: 'https://api.example.com',
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 10),
  ));
  dio.interceptors.add(LogInterceptor(responseBody: true));
  ref.onDispose(() => dio.close());
  return dio;
});

// =============================================================================
// 2. 数据模型 (使用 Freezed 生成)
// =============================================================================

// user.dart — 实际项目中由 freezed 生成
class User {
  final String id;
  final String name;
  final String email;

  const User({
    required this.id,
    required this.name,
    required this.email,
  });

  factory User.fromJson(Map<String, dynamic> json) => User(
        id: json['id'] as String,
        name: json['name'] as String,
        email: json['email'] as String,
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'name': name,
        'email': email,
      };
}

// =============================================================================
// 3. Repository 层
// =============================================================================

class UserRepository {
  final Dio _dio;

  UserRepository(this._dio);

  Future<List<User>> fetchUsers() async {
    final response = await _dio.get('/users');
    return (response.data as List).map((e) => User.fromJson(e)).toList();
  }

  Future<User> fetchUserById(String id) async {
    final response = await _dio.get('/users/$id');
    return User.fromJson(response.data);
  }

  Future<User> createUser({required String name, required String email}) async {
    final response = await _dio.post('/users', data: {
      'name': name,
      'email': email,
    });
    return User.fromJson(response.data);
  }
}

final userRepositoryProvider = Provider<UserRepository>((ref) {
  return UserRepository(ref.read(dioProvider));
});

// =============================================================================
// 4. Controller / ViewModel 层
// =============================================================================

class UserListController extends Notifier<AsyncValue<List<User>>> {
  @override
  AsyncValue<List<User>> build() => const AsyncValue.loading();

  Future<void> loadUsers() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() => ref.read(userRepositoryProvider).fetchUsers());
  }

  Future<void> addUser(String name, String email) async {
    final repo = ref.read(userRepositoryProvider);
    await repo.createUser(name: name, email: email);
    await loadUsers(); // 刷新列表
  }
}

final userListControllerProvider =
    NotifierProvider<UserListController, AsyncValue<List<User>>>(
  UserListController.new,
);

// =============================================================================
// 5. Widget 层
// =============================================================================

// 页面入口
class UserListPage extends ConsumerWidget {
  const UserListPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final usersAsync = ref.watch(userListControllerProvider);

    ref.listen(userListControllerProvider, (prev, next) {
      next.whenOrNull(
        error: (err, stack) {
          // 全局错误处理
          print('Error loading users: $err');
        },
      );
    });

    return Scaffold(
      appBar: AppBar(title: const Text('Users')),
      body: usersAsync.when(
        data: (users) => ListView.builder(
          itemCount: users.length,
          itemBuilder: (context, index) => ListTile(
            title: Text(users[index].name),
            subtitle: Text(users[index].email),
          ),
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('Error: $error'),
              ElevatedButton(
                onPressed: () =>
                    ref.read(userListControllerProvider.notifier).loadUsers(),
                child: const Text('Retry'),
              ),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _showAddUserDialog(context, ref),
        child: const Icon(Icons.add),
      ),
    );
  }

  void _showAddUserDialog(BuildContext context, WidgetRef ref) {
    // 仅示例，实际应提取为独立的 Dialog Widget
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Add User'),
        content: const Text('Dialog implementation'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Cancel'),
          ),
        ],
      ),
    );
  }
}

// =============================================================================
// 6. 带参数查询 (family)
// =============================================================================

final userDetailProvider =
    FutureProvider.autoDispose.family<User, String>((ref, userId) async {
  final repo = ref.read(userRepositoryProvider);
  return repo.fetchUserById(userId);
});

class UserDetailPage extends ConsumerWidget {
  final String userId;
  const UserDetailPage({super.key, required this.userId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsync = ref.watch(userDetailProvider(userId));
    return Scaffold(
      appBar: AppBar(title: const Text('User Detail')),
      body: userAsync.when(
        data: (user) => Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Name: ${user.name}', style: const TextStyle(fontSize: 18)),
              const SizedBox(height: 8),
              Text('Email: ${user.email}'),
            ],
          ),
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, _) => Center(child: Text('Error: $error')),
      ),
    );
  }
}
