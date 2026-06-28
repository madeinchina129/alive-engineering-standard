# Go 命名规范细则

## 包命名规则

### 包名规范

```go
// ✅ 正确：小写、单数、描述性
package user
package http
package crypto

// ❌ 错误：大写、复数、下划线、无意义
package User        // ❌
package users       // ❌
package my_package  // ❌
package util        // ❌ 过于泛义
package common      // ❌ 过于泛义
```

### 避免包名冲突

```go
// ✅ 正确：导入别名避免冲突
import (
    "crypto/rand"
    mrand "math/rand"  // 别名
)
```

### 包名与目录名一致

```go
// 目录: internal/user/
// 包名: package user
```

## 类型命名

```go
// ✅ 正确：PascalCase，名词
type User struct{}
type HttpClient struct{}
type PaginationParams struct{}

// ✅ 正确：接口以 -er 结尾
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
type Logger interface { Log(msg string) }
```

## 函数命名

```go
// ✅ 正确：动词或动词+名词
func GetUser(id int) *User {}
func CreateUser(u *User) error {}
func (u *User) UpdateName(name string) {}

// ✅ 正确：测试函数
func TestGetUser(t *testing.T) {}
func BenchmarkGetUser(b *testing.B) {}
```

## 强制规则 (MUST)

### 1. 接收者命名 1-3 字母

```go
// ✅ 正确：简短接收者
func (u *User) FullName() string {
    return u.FirstName + " " + u.LastName
}

func (s *UserService) GetUser(id int) (*User, error) {
    return s.repo.FindByID(id)
}

// ❌ 错误：过长或混合
func (user *User) FullName() string {}    // ❌ user 过长
func (self *User) FullName() string {}    // ❌ self 非 Go 风格
func (u *User) GetFullName() string {}    // ❌ 冗余 Get
```

### 2. 常量使用 PascalCase

```go
// ✅ 正确
const (
    MaxRetries    = 3
    DefaultPort   = 8080
    StatusActive  = "active"
)

// ❌ 错误：全大写或下划线
const MAX_RETRIES = 3     // ❌
const default_port = 8080 // ❌
```

### 3. 变量名随作用域变化

```go
// ✅ 正确：作用域越小，名字越短
var c int  // 包级变量：简短（作用域大，但使用频率高）

func process() {
    var userID int    // 函数级：描述性
    for i := 0; i < 10; i++ {  // 块级：一个字母
        // ...
    }
}
```

### 4. 布尔字段/函数使用 Is/Has/Can 前缀

```go
// ✅ 正确
type User struct {
    IsActive  bool
    HasPermission bool
}

func IsValid(email string) bool {}
func HasPermission(userID string, perm string) bool {}
func CanEdit(userID string) bool {}
```

### 5. 避免冗余词汇

```go
// ✅ 正确：不包含包名冗余
// package user
func Get(id int) *User {}     // user.Get() 而非 user.GetUser()
type Service struct{}          // user.Service 而非 user.UserService

// ❌ 错误：冗余
func GetUser(id int) *User {} // user.GetUser() → 重复
```

## 推荐实践 (SHOULD)

### 1. 方法接收者使用指针还是值

```go
// ✅ 需要修改接收者或接收者很大 → 指针
func (u *User) UpdateEmail(email string) { u.Email = email }

// ✅ 不修改且接收者小 → 值
func (u User) FullName() string { return u.FirstName + " " + u.LastName }
```

### 2. 接口命名避免后缀污染

```go
// ✅ 正确：单一方法接口用 -er
type Reader interface { Read(p []byte) (n int, err error) }

// ✅ 多方法接口用完整名称
type Storage interface {
    Save(key string, data []byte) error
    Load(key string) ([]byte, error)
    Delete(key string) error
}
```

## 禁止行为 (MUST NOT)

- ❌ snake_case 命名（除测试文件）
- ❌ 全大写常量名（`MAX_RETRIES`）
- ❌ 接收者用 `self` 或 `this`
- ❌ 包名用 `util`、`common`、`misc`
- ❌ 包名和目录名不一致
- ❌ 公有函数名包含包名冗余
