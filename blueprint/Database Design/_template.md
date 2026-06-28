# 数据库设计：[模块名称]

> 版本：1.0 | 数据库：PostgreSQL 16 | 最后更新：YYYY-MM-DD

---

## 1. 数据库选型

| 组件 | 选型 | 版本 | 用途 |
|------|------|------|------|
| 主库 | PostgreSQL | 16 | 业务数据 |
| 缓存 | Redis | 7 | 会话/热点数据 |
| 文档库 | MongoDB | 7 | 非结构化数据 |

## 2. 数据库连接

**主库**：
- Host: `{host}`
- Port: `5432`
- Database: `alive_{module}`
- Pool: `10-50`

## 3. 命名规范

| 对象 | 命名规则 | 示例 |
|------|----------|------|
| 数据库 | `alive_{module}` | `alive_user` |
| 表 | `t_{module}_{entity}` | `t_user_account` |
| 字段 | `snake_case` | `created_at` |
| 主键 | `pk_{table}` | `pk_user_account` |
| 索引 | `idx_{table}_{column}` | `idx_user_account_email` |
| 外键 | `fk_{table}_{ref_table}` | `fk_user_account_user` |
| 序列 | `seq_{table}_{column}` | `seq_user_account_id` |

## 4. 迁移策略

### 4.1 版本管理
- 使用 Flyway / Liquibase
- 命名格式：`V{version}__{description}.sql`
- 示例：`V20240628__create_user_account.sql`

### 4.2 迁移文件结构
```
database/migration/
├── V1__init.sql
├── V2__user.sql
├── V3__alive.sql
├── V4__report.sql
└── V5__seed.sql
```

## 5. 备份策略

| 类型 | 频率 | 保留 | 方式 |
|------|------|------|------|
| 全量备份 | 每日 | 30 天 | pg_dump |
| WAL 归档 | 持续 | 7 天 | 持续归档 |
| 逻辑备份 | 每周 | 90 天 | pg_dump --format=custom |

## 6. SQL 审查要点

- [ ] 所有查询使用 EXPLAIN ANALYZE 验证
- [ ] JOIN 字段必须有索引
- [ ] 避免 SELECT *
- [ ] UPDATE/DELETE 必须有 WHERE 条件
- [ ] 大表操作必须分批执行
- [ ] 事务范围尽可能小
