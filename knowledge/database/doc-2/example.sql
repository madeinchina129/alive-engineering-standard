```sql
-- Migration V1.2.3: 拆分用户地址到独立表

-- 前置检查
-- 检查表大小
SELECT COUNT(*) FROM user_address_old;

-- Up Migration
START TRANSACTION;

-- 1. 创建新表
CREATE TABLE user_address (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    address_type TINYINT NOT NULL COMMENT '1=收货地址 2=发票地址',
    province VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    district VARCHAR(50) NOT NULL,
    detail VARCHAR(500) NOT NULL,
    is_default TINYINT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. 数据迁移（分批）
INSERT INTO user_address (user_id, address_type, province, city, district, detail, is_default, created_at)
SELECT user_id, 1, province, city, district, detail, is_default, created_at
FROM user_old WHERE province IS NOT NULL
LIMIT 1000;

-- 3. 数据校验
SELECT COUNT(*) FROM (
    SELECT id FROM user_old WHERE province IS NOT NULL
    EXCEPT
    SELECT DISTINCT user_address.user_id FROM user_address
) AS diff;  -- 期望: 0

COMMIT;

-- Down Migration
START TRANSACTION;
-- DROP TABLE IF EXISTS user_address;
-- ALTER TABLE user_old ADD ... (恢复原结构)
COMMIT;
```