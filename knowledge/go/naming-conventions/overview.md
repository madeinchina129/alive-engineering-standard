# Go 命名规范

## 为什么需要 Go 命名规范

Go 的命名哲学是"短胜于长，清晰胜过晦涩"。与其他语言不同，Go 使用大小写控制访问权限，命名风格直接影响代码的可读性和可维护性。

### 大小写的语义

```go
// 大写开头 = 公开（exported）
func PublicFunc() {}
type PublicType struct{}
var PublicVar = 1
const PublicConst = "public"

// 小写开头 = 私有（unexported）
func privateFunc() {}
type privateType struct{}
var privateVar = 1
```

### 驼峰命名

Go 使用驼峰命名（CamelCase），不使用下划线（snake_case）：

```go
// ✅ 正确：驼峰命名
type UserProfile struct{}
func getUserByID(id int) {}

// ❌ 错误：下划线命名
type User_profile struct{}     // ❌
func get_user_by_id(id int) {} // ❌
```

### 短变量名

```go
// ✅ 正确：短变量名（作用域越小，名字越短）
for i := 0; i < 10; i++ { }        // i 作用域限于 for 块
r, err := http.Get(url)             // r 作用域限于当前函数
conf := loadConfig(path)            // conf 常用缩写

// ❌ 错误：过长或不一致
for index := 0; index < 10; index++ { }  // ❌ index 在短作用域中过长
```

---

## 命名规则对比

| 元素 | 规则 | 示例 |
|------|------|------|
| 包名 | 小写、单数 | `user`, `http`, `fmt` |
| 类型 | PascalCase | `User`, `HttpClient` |
| 函数 | PascalCase（公开）/ camelCase（私有） | `GetUser()`, `getUser()` |
| 变量 | camelCase | `userName`, `httpClient` |
| 常量 | PascalCase | `MaxRetries`, `DefaultTimeout` |
| 接口 | PascalCase + -er 后缀 | `Reader`, `Writer`, `Logger` |
| 接收者 | 1-2 字母 | `u User`, `r Reader` |

---

## 适用范围

- **强制使用**：所有 Go 项目
- **工具**：`golint`、`go vet`、`staticcheck` 自动检查
