# Swift Codable FAQ

## Q: 什么时候需要自定义 CodingKeys？

当 JSON 键和 Swift 属性名不一致时：

```swift
// JSON: { "user_id": 1, "full_name": "Alice" }
struct User: Codable {
    let userID: Int
    let fullName: String
    
    enum CodingKeys: String, CodingKey {
        case userID = "user_id"
        case fullName = "full_name"
    }
}

// 或用 keyDecodingStrategy = .convertFromSnakeCase 自动转换
```

## Q: `decodeIfPresent` 和 `decode` 的区别？

```
decode：字段必须存在，否则抛错
decodeIfPresent：字段可选，不存在则为 nil
```

```swift
let port = try container.decodeIfPresent(Int.self, forKey: .port) ?? 8080
```

## Q: 如何处理 Date 格式？

```swift
// ISO 8601
decoder.dateDecodingStrategy = .iso8601

// 自定义格式
let formatter = DateFormatter()
formatter.dateFormat = "yyyy-MM-dd"
decoder.dateDecodingStrategy = .formatted(formatter)

// 时间戳
decoder.dateDecodingStrategy = .secondsSince1970
```

## Q: 如何忽略 JSON 中多余的字段？

默认 Codable 会忽略多余字段。如果不需要反向兼容性，可以添加：

```swift
struct User: Codable {
    let id: Int
    let name: String
    // 其他字段自动忽略
}
```

## Q: 嵌套 JSON 如何解码？

```swift
struct ApiResponse<T: Codable>: Codable {
    let data: T
    let message: String
}

struct User: Codable {
    let id: Int
    let name: String
}

// JSON: { "data": { "id": 1, "name": "Alice" }, "message": "ok" }
let response = try decoder.decode(ApiResponse<User>.self, from: data)
```
