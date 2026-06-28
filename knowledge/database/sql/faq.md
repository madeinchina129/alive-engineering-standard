# SQL 优化指南 — FAQ

## Q1: 如何分析 SQL 性能？
使用 EXPLAIN ANALYZE（MySQL 8.0.18+ / PostgreSQL）查看实际执行计划和耗时。关注 type 字段（ALL=全表扫描需优化）、rows（扫描行数）和 Extra（Using filesort/Using temporary 需优化）。

## Q2: 索引加了查询还是慢？
可能原因：① 索引选择性差（重复值太多）② WHERE 条件用了 OR 导致索引失效 ③ 查询返回行数过多 ④ 索引碎片严重（需重建）。

## Q3: LIKE 模糊查询能用索引吗？
前缀匹配（LIKE 'abc%'）可以用索引。后缀匹配（LIKE '%abc'）和包含匹配（LIKE '%abc%'）不能用 B+Tree 索引。后缀匹配需求使用倒排索引（全文索引或 Elasticsearch）。
