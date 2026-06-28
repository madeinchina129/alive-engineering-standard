@HiveType(typeId: 0)
class User extends HiveObject {
  @HiveField(0)
  final String name;
  @HiveField(1)
  final int age;
}