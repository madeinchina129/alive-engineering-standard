import 'package:flutter_riverpod/flutter_riverpod.dart';
final orderProvider = Provider<OrderService>((ref) {
  return OrderService();
});