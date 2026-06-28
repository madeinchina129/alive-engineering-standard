/// 数据模型
/// 自动生成于 2026-06-28 17:24 | 版本：1.0
library;

class ExampleModel {
    final String id;
    final String name;
    final DateTime createdAt;
  
  const ExampleModel({
        required this.id,
        required this.name,
        required this.createdAt,
      });

  factory ExampleModel.fromJson(Map<String, dynamic> json) {
    return ExampleModel(
            id: json['id'] as String,
            name: json['name'] as String,
            createdAt: json['createdAt'] as DateTime,
          );
  }

  Map<String, dynamic> toJson() {
    return {
            'id': id,
            'name': name,
            'createdAt': createdAt,
          };
  }

  @override
  String toString() => 'ExampleModel({ id: $id, name: $name, createdAt: $createdAt })';

  ExampleModel.copyWith({
        String? id,
        String? name,
        DateTime? createdAt,
      }) {
    return ExampleModel(
            id: id ?? this.id,
            name: name ?? this.name,
            createdAt: createdAt ?? this.createdAt,
          );
  }
}