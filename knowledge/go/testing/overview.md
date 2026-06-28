# Go 测试规范

## Go 测试基础

Go 内置 `testing` 包，无需第三方测试框架：

```go
// 测试文件：*_test.go
// 测试函数：func TestXxx(t *testing.T)

// math_test.go
func TestAdd(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d; want 5", result)
    }
}
```

### 测试组织

```
src/
├── math.go
├── math_test.go        # 单元测试（同包）
├── math_internal_test.go # 测试私有函数（可选）
tests/
├── integration_test.go  # 集成测试（单独包）
```

---

## 测试类型

| 类型 | 写法 | 用途 |
|------|------|------|
| 单元测试 | `func TestXxx(t *testing.T)` | 函数/方法测试 |
| 表驱动测试 | `[]struct{name, args, want}` | 多输入组合 |
| 基准测试 | `func BenchmarkXxx(b *testing.B)` | 性能测试 |
| 示例函数 | `func ExampleXxx()` | 文档示例 |
| TestMain | `func TestMain(m *testing.M)` | 全局 setup/teardown |

---

## 适用范围

- **所有 Go 包**：必须包含测试
- **覆盖率目标**：核心逻辑 80%+，整体 60%+
