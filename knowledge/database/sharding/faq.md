# NoSQL 数据库设计 — FAQ

## Q1: 什么时候用 MongoDB 什么时候用 MySQL？
MongoDB 适合：文档数据、灵活 Schema、快速迭代。MySQL 适合：强一致性需求、复杂 JOIN 和事务、结构化数据。一个好的架构经常同时使用两者（Polyglot Persistence）。

## Q2: Redis 缓存什么数据？
热点数据（频繁访问但不常变更）、Session 数据、计数器（点赞/阅读量）、分布式锁、限流器。不适合：全量数据、需要持久化保证的数据、大 Key（>10MB）。
