# Rust 所有权与借用规范

## 所有权三原则

Rust 的所有权系统是内存安全的基石，编译器在编译期检查以下三条规则：

1. **每个值在 Rust 中都有一个所有者（owner）**
2. **同一时间只能有一个所有者**
3. **当所有者离开作用域时，值被自动释放**

```rust
// 所有权转移
let s1 = String::from("hello");
let s2 = s1;            // s1 的所有权转移到 s2
// println!("{s1}");    // ❌ 编译错误：s1 已失效
println!("{s2}");        // ✅ s2 是所有者
```

```rust
// 借用：使用值而不获取所有权
fn calculate_length(s: &String) -> usize {
    s.len()  // s 是借用，不获取所有权
}

let s1 = String::from("hello");
let len = calculate_length(&s1);
println!("{s1} 的长度是 {len}");  // ✅ s1 仍然有效
```

---

## 所有权和借用对比

| 操作 | 所有权限 | 调用方状态 | 使用场景 |
|------|---------|-----------|---------|
| 转移所有权 `s2 = s1` | s2 获得所有权 | s1 失效 | 需要完全拥有值 |
| 不可变借用 `&s` | 调用方保留 | 可继续使用 | 只读访问 |
| 可变借用 `&mut s` | 调用方保留 | 借出期间不可用 | 需要修改值 |
| 克隆 `s1.clone()` | 双方各有副本 | 双方都有效 | 需要完整副本 |

---

## 生命周期标注规则

```rust
// 函数返回引用时需要标注生命周期
fn first_word<'a>(text: &'a str) -> &'a str {
    text.split_whitespace().next().unwrap_or("")
}

// 结构体包含引用时需要标注
struct User<'a> {
    name: &'a str,
    id: &'a str,
}
```

---

## 适用范围

- **强制使用**：所有 Rust 项目
- **工具**：`cargo clippy`、`cargo fmt`、`rustc` 编译器检查
