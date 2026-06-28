# Swift Codable 序列化规范

## Codable 基础

Swift 的 `Codable`（`Encodable & Decodable`）协议提供声明式 JSON 序列化：

```swift
// ✅ 自动遵循 Codable
struct User: Codable {
    let id: Int
    let name: String
    let email: String
    let createdAt: Date
}

// 编码
let user = User(id: 1, name: "Alice", email: "alice@example.com", createdAt: Date())
let encoder = JSONEncoder()
encoder.dateEncodingStrategy = .iso8601
let data = try encoder.encode(user)

// 解码
let decoder = JSONDecoder()
decoder.dateDecodingStrategy = .iso8601
let decoded = try decoder.decode(User.self, from: data)
```

### 核心协议

```
Codable = Encodable (编码) + Decodable (解码)
                      ↓                ↓
            encode(to:)  ←→  init(from:)
```

---

## 编码策略对比

| 策略 | JSON 键 | 示例 |
|------|---------|------|
| 默认 | Swift 属性名 | `createdAt` |
| convertToSnakeCase | 蛇形命名 | `created_at` |
| 自定义 | CodingKeys 枚举 | 任意映射 |

---

## 适用范围

- **网络 API 响应解析**
- **本地数据持久化**（UserDefaults、文件）
- **JSON 配置解析**
