# Hive 本地存储规范

## 概述
Hive 是 Flutter 轻量级高性能 NoSQL 存储方案的推荐选择。

## 核心原则
1. Box 设计：每个业务实体对应独立 Box
2. 类型安全：所有自定义类型注册 TypeAdapter
3. 性能优先：合理使用 lazy Box 和 compaction

## 适用范围
适用于本项目中所有相关场景。
