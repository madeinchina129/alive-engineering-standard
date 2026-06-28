```sql
-- 审计日志表设计
CREATE TABLE audit_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id VARCHAR(64) NOT NULL,
    user_ip VARCHAR(45) NOT NULL,
    action_type ENUM('CREATE', 'READ', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT', 'PERMISSION_CHANGE') NOT NULL,
    object_type VARCHAR(64) NOT NULL COMMENT '操作对象类型，如 order, user, product',
    object_id VARCHAR(64) NOT NULL COMMENT '操作对象 ID',
    detail JSON COMMENT '操作详情',
    result ENUM('SUCCESS', 'FAILURE', 'DENIED') NOT NULL,
    checksum VARCHAR(64) NOT NULL COMMENT '前一条日志的 hash 值，形成链式结构',
    INDEX idx_timestamp (timestamp),
    INDEX idx_user (user_id),
    INDEX idx_action (action_type, object_type),
    INDEX idx_object (object_type, object_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```