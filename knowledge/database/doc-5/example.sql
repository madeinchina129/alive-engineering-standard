```sql
-- 数据仓库分层设计：电商业务

-- ODS 层：数据源原始数据
CREATE TABLE ods_order (
    order_id STRING,
    order_data STRING COMMENT '原始JSON',
    etl_time TIMESTAMP
);

-- DWD 层：清洗后的明细数据
CREATE TABLE dwd_order_detail (
    order_id STRING COMMENT '订单ID',
    user_id STRING COMMENT '用户ID',
    product_id STRING COMMENT '商品ID',
    order_amount DECIMAL(12,2) COMMENT '订单金额',
    order_status STRING COMMENT '订单状态',
    pay_time TIMESTAMP COMMENT '支付时间',
    dt STRING COMMENT '分区日期'
) PARTITIONED BY (dt STRING);

-- DWS 层：日汇总表
CREATE TABLE dws_order_daily (
    dt STRING COMMENT '日期',
    total_order_count BIGINT COMMENT '订单总数',
    total_order_amount DECIMAL(16,2) COMMENT '订单总金额',
    paid_order_count BIGINT COMMENT '已支付订单数',
    paid_rate DECIMAL(5,4) COMMENT '支付转化率',
    avg_order_amount DECIMAL(12,2) COMMENT '平均订单金额'
) PARTITIONED BY (dt STRING);

-- ADS 层：业务报表
CREATE TABLE ads_daily_report (
    dt STRING COMMENT '日期',
    gmv DECIMAL(16,2) COMMENT 'GMV',
    order_count BIGINT COMMENT '订单量',
    paid_user_count BIGINT COMMENT '支付用户数',
    new_user_count BIGINT COMMENT '新增用户数',
    arpu DECIMAL(12,2) COMMENT '每用户平均收入'
) PARTITIONED BY (dt STRING);
```