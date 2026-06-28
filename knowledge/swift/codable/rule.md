# Swift Codable 细则

## 强制规则 (MUST)

### 1. 使用 CodingKeys 处理命名差异

```swift
// ✅ 正确：CodingKeys 明确映射
struct User: Codable {
    let id: Int
    let fullName: String
    
    enum CodingKeys: String, CodingKey {
        case id
        case fullName = "full_name"  // JSON 键映射
    }
}

// ❌ 错误：依赖 JSON 键和属性名完全一致（脆弱）
struct User: Codable {
    let full_name: String  // ❌ Swift 属性应使用驼峰
}
```

### 2. JSONDecoder 配置全局策略

```swift
// ✅ 正确：统一配置 decoder
extension JSONDecoder {
    static let `default`: JSONDecoder = {
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        decoder.dateDecodingStrategy = .iso8601
        return decoder
    }()
}

// ❌ 错误：每次都手动配置
let decoder = JSONDecoder()
decoder.keyDecodingStrategy = .convertFromSnakeCase  // ❌ 重复代码
```

### 3. 处理可选值和默认值

```swift
// ✅ 正确：可选值处理
struct Config: Codable {
    let host: String
    let port: Int?
    let timeout: Int
    
    enum CodingKeys: String, CodingKey {
        case host, port, timeout
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        host = try container.decode(String.self, forKey: .host)
        port = try container.decodeIfPresent(Int.self, forKey: .port)
        timeout = try container.decodeIfPresent(Int.self, forKey: .timeout) ?? 30
    }
}

// ❌ 错误：port 字段不存在时解码失败
struct Config: Codable {
    let host: String
    let port: Int  // ❌ JSON 中没有 port 字段会抛错
}
```

### 4. 自定义编解码实现复杂类型

```swift
// ✅ 正确：自定义 init(from:) 实现
struct DateWrapper: Codable {
    let date: Date
    
    init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()
        let timestamp = try container.decode(Double.self)
        date = Date(timeIntervalSince1970: timestamp)
    }
    
    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        try container.encode(date.timeIntervalSince1970)
    }
}
```

## 推荐实践 (SHOULD)

### 使用 typealias 简化

```swift
typealias JSONDictionary = [String: Any]
```

## 禁止行为 (MUST NOT)

- ❌ 手动实现 Codable 所有方法（除非必要）
- ❌ 使用 `[String: Any]` 代替 Codable 结构体
- ❌ 不使用 CodingKeys 而依赖属性名匹配
- ❌ 解码时不处理可选值导致 crash
