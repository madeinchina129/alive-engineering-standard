```javascript
// MongoDB 文档设计 - 博客系统
// 内嵌设计（推荐）
const post = {
  _id: ObjectId("..."),
  title: "NoSQL 设计指南",
  content: "在 NoSQL 中...",
  author: {
    id: ObjectId("..."),
    name: "张三",  // 冗余：避免每次查询用户
    avatar: "url"
  },
  tags: ["nosql", "database", "mongodb"],
  stats: {
    views: 12345,
    likes: 678,
    comments: 90
  },
  created_at: ISODate("2024-01-15"),
  updated_at: ISODate("2024-01-16")
};

// 索引设计
db.posts.createIndex({ tags: 1, created_at: -1 });
db.posts.createIndex({ "author.id": 1 });
db.posts.createIndex({ "stats.views": -1 });
```

```bash
# Redis 缓存策略
# 用户会话缓存（15 分钟过期）
SETEX user:1001:session 900 "{"token":"xxx","role":"admin"}"

# 热点数据缓存（1 小时过期）
SETEX product:2001:detail 3600 "{\"id\":2001,\"name\":\"商品\"}"

# 计数器
INCR article:3001:views
EXPIRE article:3001:views 86400  # 24h 过期

# 分布式锁
SET lock:order:pay:1001 "worker1" NX EX 30
```