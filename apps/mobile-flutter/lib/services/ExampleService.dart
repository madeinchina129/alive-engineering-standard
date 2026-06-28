/// API 服务
/// 自动生成于 2026-06-28 17:24
library;

import 'package:dio/dio.dart';
import '../models/ExampleModel.dart';

class ExampleService {
  final Dio _dio;

  ExampleService(this._dio);

    Future<List<ExampleModel>> getList({
    int page = 1,
    int pageSize = 20,
  }) async {
    final response = await _dio.get('/api/v1/examples', queryParameters: {
      'page': page,
      'page_size': pageSize,
    });
    return (response.data['data'] as List)
        .map((e) => ExampleModel.fromJson(e))
        .toList();
  }
  
    Future<ExampleModel> getDetail(String id) async {
    final response = await _dio.get('/api/v1/examples/$id');
    return ExampleModel.fromJson(response.data['data']);
  }
  
    Future<ExampleModel> create(Map<String, dynamic> data) async {
    final response = await _dio.post('/api/v1/examples', data: data);
    return ExampleModel.fromJson(response.data['data']);
  }
  
    Future<ExampleModel> update(String id, Map<String, dynamic> data) async {
    final response = await _dio.put('/api/v1/examples/$id', data: data);
    return ExampleModel.fromJson(response.data['data']);
  }
  
    Future<void> delete(String id) async {
    await _dio.delete('/api/v1/examples/$id');
  }
  }