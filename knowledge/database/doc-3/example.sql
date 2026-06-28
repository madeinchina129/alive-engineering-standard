```sql
-- 数据字典示例
-- 表名: user_account
-- 业务含义: 平台用户账户信息

-- | 字段名 | 类型 | 必填 | 默认值 | 业务含义 | 取值范围 |
-- |--------|------|------|--------|----------|----------|
-- | id | BIGINT | Y | - | 用户ID（自增） | - |
-- | username | VARCHAR(50) | Y | - | 用户名 | 字母数字下划线 |
-- | email | VARCHAR(200) | Y | - | 邮箱 | 有效邮箱格式 |
-- | phone | VARCHAR(20) | N | NULL | 手机号 | 11位数字 |
-- | status | TINYINT | Y | 0 | 状态 | 0=未激活 1=正常 2=锁定 3=已删除 |
-- | user_type | TINYINT | Y | 1 | 类型 | 1=个人 2=企业 3=管理员 |
-- | password_hash | VARCHAR(255) | Y | - | 密码哈希 | bcrypt 哈希值 |
-- | created_at | DATETIME | Y | CURRENT_TIMESTAMP | 注册时间 | UTC |
-- | updated_at | DATETIME | Y | - | 最后更新时间 | UTC |

CREATE TABLE user_account (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) NOT NULL COMMENT '用户名',
    email VARCHAR(200) NOT NULL COMMENT '邮箱',
    phone VARCHAR(20) NULL COMMENT '手机号',
    status TINYINT NOT NULL DEFAULT 0 COMMENT '状态: 0=未激活 1=正常 2=锁定 3=已删除',
    user_type TINYINT NOT NULL DEFAULT 1 COMMENT '类型: 1=个人 2=企业 3=管理员',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希(bcrypt)',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间(UTC)',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间(UTC)',
    UNIQUE INDEX idx_username (username),
    UNIQUE INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户账户表';
```