# Go 命名 FAQ

## Q: Go 为什么不用下划线？

Go 核心团队在设计时就选择了驼峰命名。下划线在 Go 中主要用于：
- `_` 空白标识符（忽略返回值）
- `_` 导入副作用（`import _ "image/png"`）
- 生成代码（protobuf、swagger）

## Q: 包名叫什么好？

包名应该描述包提供的内容，而不是包的内容类型：

```go
// ✅ 好：描述功能
package user     // 提供用户相关操作
package http     // 提供 HTTP 客户端/服务端
package crypto   // 提供加密功能

// ❌ 差：模糊或泛义
package utils     // 什么都装
package common    // 什么都装
package helpers   // 什么都装
```

## Q: 为什么变量名要随作用域变短？

```go
// 包级变量需要更多上下文
var db *sql.DB

func GetUser(id string) (*User, error) {
    // 函数级变量需要描述性
    var user *User
    
    for i := 0; i < len(users); i++ {
        // 块级变量 i 足够清晰
    }
}
```

缩短变量名减少视觉噪音，但须保证含义清晰。

## Q: GetUser 和 Get 的区别？

```go
package user

// 如果包名叫 user，在外部调用时已经是 user.Get()
// 所以函数名 GetUser 是冗余的
func Get(id int) *User {}     // ✅ user.Get()
func GetUser(id int) *User {} // ❌ user.GetUser()
```

## Q: 接口命名一定用 -er 后缀吗？

单方法接口用 -er 是惯例，多方法接口可以灵活命名：

```go
// 单方法 - 推荐 -er
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }

// 多方法 - 完整名称
type Storage interface { Save(); Load(); Delete() }
type Repository interface { FindByID(); Save(); Delete() }
```

## Q: 接收者用 `this` 或 `self` 可以吗？

不推荐。Go 中的惯用风格是用类型首字母缩写：

```go
type User struct{}

func (u *User) Name() string {} // ✅ Go 风格：类型首字母

// ❌ 非 Go 风格
func (this *User) Name() string {} // ❌ 像 Java
func (self *User) Name() string {} // ❌ 像 Python
```
