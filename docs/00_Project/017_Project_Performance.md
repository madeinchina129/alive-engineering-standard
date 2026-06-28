# 性能基线标准

> 版本: v1.0 | 更新: 2026-06

## 概述

本文定义项目的性能目标、基线指标和性能退化防控规范。所有服务在交付前必须满足本文定义的性能门槛。

## 核心原则

### 1. 可测量

- 每一个性能要求必须有明确的测量指标和阈值
- 测量方法必须可复现
- 测量环境必须与环境基线保持一致

### 2. 基线驱动

- 每个版本发布前必须对比性能基线
- 性能退化超过 5% 必须解释原因
- 累计退化 10% 阻止版本发布

### 3. 左移

- 性能测试从编码阶段开始
- 单元测试中包含性能断言
- CI 流水线中集成基准测试

## 通用性能目标

### API 响应时间

| 端点类型 | P50 | P95 | P99 | 吞吐量 |
|----------|-----|-----|-----|--------|
| 简单查询（单表） | < 50ms | < 100ms | < 200ms | > 1000 rps |
| 复杂查询（多表关联） | < 200ms | < 500ms | < 1000ms | > 200 rps |
| 写入操作 | < 100ms | < 300ms | < 500ms | > 500 rps |
| 批量操作 | < 1000ms | < 3000ms | < 5000ms | > 50 rps |
| 第三方代理 | < 500ms | < 2000ms | < 5000ms | > 100 rps |

### 前端性能

| 指标 | 目标 | 警戒 |
|------|------|------|
| FCP (First Contentful Paint) | < 1.5s | > 2.5s |
| LCP (Largest Contentful Paint) | < 2.5s | > 4.0s |
| TTI (Time to Interactive) | < 3.5s | > 5.0s |
| TBT (Total Blocking Time) | < 200ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | > 0.25 |
| 首屏 JS 体积 | < 200KB | > 400KB |

### 数据库性能

| 指标 | 目标 | 警戒 |
|------|------|------|
| 慢查询 (>1s) 数量 | 0 | > 5 条/天 |
| 连接池使用率 | < 60% | > 80% |
| 缓存命中率 | > 90% | < 80% |
| 复制延迟 | < 100ms | > 5s |

## 性能预算

### API 预算

```
GET /api/v1/users/{id} — 预算: 50ms P95
  ├── 数据库查询:    10ms (20%)
  ├── 缓存查询:      5ms  (10%)
  ├── 序列化/反序列化: 15ms (30%)
  ├── 业务逻辑:      10ms (20%)
  └── 网络开销:      10ms (20%)
```

### 页面预算

```
用户列表页面 — 预算: 1500ms FCP
  ├── HTML:          80KB  (200ms)
  ├── CSS:           40KB  (100ms)
  ├── JS Core:       120KB (400ms)
  ├── JS 页面代码:    80KB  (300ms)
  ├── API 数据加载:         (300ms)
  └── 渲染:                 (200ms)
```

## 性能测试

### 单元级性能测试

```java
@Test
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@Warmup(iterations = 3, time = 1)
@Measurement(iterations = 5, time = 2)
public void benchmarkUserSerialization(Blackhole bh) {
    User user = createTestUser();
    for (int i = 0; i < 1000; i++) {
        bh.consume(mapper.writeValueAsString(user));
    }
}
```

### API 级性能测试

```yaml
# Gatling 场景示例
scenarios:
  - name: "用户列表查询"
    duration: 5m
    users: 100
    rampUp: 30s
    thresholds:
      - "P95 < 200ms"
      - "success_rate > 99.9%"
```

## 性能退化防控

### 阈值策略

```
┌──────────────────────────────────────┐
│ 每个版本自动执行性能基线对比           │
│                                      │
│ 退化 < 3%  ── 警告，人工确认          │
│ 退化 3-5%  ── 必须解释原因            │
│ 退化 5-10% ── 需架构组审批            │
│ 退化 > 10% ── 阻止合并                │
└──────────────────────────────────────┘
```

### 性能回归检测

- CI 中每次合并前执行性能基线测试
- 对比上一版本的基线数据
- 生成性能差异报告
- 门禁未通过则阻止合并

## 性能优化规范

### 数据库

1. 所有查询必须使用索引（通过 EXPLAIN 确认）
2. 禁止在 WHERE 条件中对索引列使用函数
3. N+1 查询必须通过 `@EntityGraph` 或 JOIN FETCH 解决
4. 批量操作必须使用 `saveAll` 而非循环 `save`

### 缓存策略

```java
// 缓存使用规则：
// 1. 高频读取、低频更新的数据 → Redis 缓存
// 2. 计算密集型结果 → 本地缓存 (Caffeine)
// 3. 配置类数据 → 本地缓存 + TTL 刷新
// 4. 用户会话 → Redis（分布式）

@Cacheable(value = "users", key = "#id", unless = "#result == null")
public User findById(Long id) {
    return repository.findById(id).orElse(null);
}
```

### 前端

1. 组件懒加载：`defineAsyncComponent`
2. 虚拟滚动：超过 1000 条列表使用
3. 图片按需加载：loading="lazy"
4. API 请求防抖：搜索等高频触发场景

## 性能问题分级

| 级别 | 定义 | 响应时间 |
|------|------|----------|
| 严重 | 核心接口 P99 > 3s | 立即修复 |
| 高 | 接口 P95 > 目标 2 倍 | 24 小时内 |
| 中 | 接口退化 5-10% | 下个版本 |
| 低 | 预算偏差 | 记录到技术债 |

## 相关文档

- [数据库规范](../09_Database/09_database_数据库规范.md)
- [缓存策略](../23_Performance/23_performance_缓存策略.md)
- [部署规范](../16_Deploy/16_deploy_部署规范.md)
