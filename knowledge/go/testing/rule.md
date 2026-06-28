# Go 测试细则

## 强制规则 (MUST)

### 1. 使用表驱动测试

```go
// ✅ 正确：表驱动测试覆盖多场景
func TestDivide(t *testing.T) {
    tests := []struct {
        name string
        a, b float64
        want float64
        err  bool
    }{
        {name: "正常除法", a: 10, b: 2, want: 5, err: false},
        {name: "除数为0", a: 10, b: 0, want: 0, err: true},
        {name: "小数", a: 7, b: 3, want: 2.3333, err: false},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Divide(tt.a, tt.b)
            if (err != nil) != tt.err {
                t.Errorf("Divide(%v,%v) err=%v; want err=%v", tt.a, tt.b, err, tt.err)
            }
            if !approxEqual(got, tt.want) {
                t.Errorf("Divide(%v,%v)=%v; want %v", tt.a, tt.b, got, tt.want)
            }
        })
    }
}

// ❌ 错误：多个测试函数重复代码
func TestDivideNormal(t *testing.T) { /* ... */ }
func TestDivideByZero(t *testing.T) { /* ... */ }
```

### 2. 测试失败用 `t.Error` / `t.Fatal`

```go
// ✅ 正确：t.Error 报告失败但继续
if got != tt.want {
    t.Errorf("got %v, want %v", got, tt.want)
}

// ✅ 正确：t.Fatal 终止测试（setup 失败时）
func TestDatabase(t *testing.T) {
    db, err := connectDB()
    if err != nil {
        t.Fatalf("无法连接数据库: %v", err)
    }
    defer db.Close()
}

// ❌ 错误：用 log.Fatal 终止测试
```

### 3. 使用 go-cmp 比较复杂结构

```go
// ✅ 正确：cmp.Diff 精确比较
import "github.com/google/go-cmp/cmp"

func TestUser(t *testing.T) {
    got := CreateUser("Alice")
    want := User{Name: "Alice", CreatedAt: time.Now()}
    if diff := cmp.Diff(want, got); diff != "" {
        t.Errorf("CreateUser mismatch (-want +got):\n%s", diff)
    }
}

// ❌ 错误：手动逐字段比较
if got.Name != want.Name || got.CreatedAt.IsZero() == false { /* ... */ }
```

### 4. 使用 TestMain 管理测试级资源

```go
// ✅ 正确：TestMain 全局 setup/teardown
func TestMain(m *testing.M) {
    setup()
    code := m.Run()
    teardown()
    os.Exit(code)
}
```

### 5. Mock 接口使用 testify/mock

```go
// ✅ 正确：testify mock
type MockRepo struct{ mock.Mock }
func (m *MockRepo) GetUser(id int) (*User, error) {
    args := m.Called(id)
    return args.Get(0).(*User), args.Error(1)
}

func TestService(t *testing.T) {
    repo := new(MockRepo)
    repo.On("GetUser", 1).Return(&User{Name: "Alice"}, nil)
    svc := NewService(repo)
    user, _ := svc.GetUser(1)
    assert.Equal(t, "Alice", user.Name)
}
```

## 推荐实践 (SHOULD)

### 辅助函数

```go
func assertEqual(t *testing.T, got, want any) {
    t.Helper()
    if !reflect.DeepEqual(got, want) {
        t.Errorf("got %v, want %v", got, want)
    }
}
```

## 禁止行为 (MUST NOT)

- ❌ 测试依赖外部服务（数据库、网络）
- ❌ 测试间共享可变状态
- ❌ 使用 `_` 忽略测试错误
