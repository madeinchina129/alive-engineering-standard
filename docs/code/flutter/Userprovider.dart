import 'package:flutter_riverpod/flutter_riverpod.dart';
final userProvider = Provider<UserService>((ref) {
  return UserService();
});