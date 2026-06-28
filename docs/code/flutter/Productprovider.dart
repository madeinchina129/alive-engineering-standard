import 'package:flutter_riverpod/flutter_riverpod.dart';
final productProvider = Provider<ProductService>((ref) {
  return ProductService();
});