```sql
-- ❌ 不好的查询
SELECT * FROM orders
WHERE YEAR(created_at) = 2024 AND MONTH(created_at) = 1
ORDER BY created_at DESC
LIMIT 20 OFFSET 1000;

-- 问题：
-- 1. SELECT * 返回不必要列
-- 2. WHERE 条件包裹了函数，无法使用索引
-- 3. LIMIT/OFFSET 大偏移量导致扫描大量行

-- ✅ 优化后的查询
SELECT id, order_no, user_id, status, total_amount, created_at
FROM orders
WHERE created_at >= '2024-01-01' AND created_at < '2024-02-01'
  AND id > 1000  -- 游标分页
ORDER BY created_at DESC, id
LIMIT 20;

-- 优化后需要的索引
ALTER TABLE orders ADD INDEX idx_created_at_id (created_at, id);
```