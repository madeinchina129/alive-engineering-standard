# Rust 所有权 FAQ

## Q: String 和 &str 的区别？

```
String     → 拥有所有权的可变字符串（堆分配）
&str       → 字符串切片引用（不拥有所有权）
&String    → String 引用（自动 deref 为 &str）
```

```rust
fn takes_owned(s: String) {}      // 获取所有权
fn takes_ref(s: &str) {}          // 借用

let s = String::from("hello");
takes_ref(&s);       // ✅ String 自动转为 &str
takes_ref("hello");  // ✅ 字面量也是 &str
takes_owned(s);      // ✅ 所有权转移
// takes_owned(&s);  // ❌ 不能用引用代替所有权
```

## Q: 什么时候用 `clone()`？

只在需要完整独立副本时使用：

```rust
// ✅ 必要：需要双方各自持有
struct User { name: String }
let user = User { name: "Alice".into() };
let name_copy = user.name.clone();  // ✅ 需要独立副本

// ❌ 不需要：借用即可
fn print_name(name: &str) {
    println!("{name}");
}
print_name(&user.name);  // ✅ 借用即可，不需要 clone
```

## Q: 为什么一个可变引用比其他引用更"特殊"？

因为数据竞争是 Rust 要消除的核心问题：

```
- 多个读（不可变引用）同时进行 → 安全 ✅
- 一个写（可变引用）时不能有读 → 防止读取过期数据 ❌
- 多个写同时进行 → 数据竞争 ❌
```

## Q: 生命周期标注 (lifetime) 什么时候需要？

三种情况需要显式标注：

```rust
// 1. 函数返回引用
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// 2. 结构体包含引用
struct Parser<'a> { content: &'a str }

// 3. impl 块
impl<'a> Parser<'a> {
    fn parse(&self) -> &'a str { self.content }
}
```

多数情况下编译器可以自动推断（省略规则）。

## Q: `Box<T>` 和 `&T` 的区别？

```
Box<T>  : 所有权在堆上，Box 在栈上指向它 → 移动 Box 时只复制指针
&T      : 借用，不拥有值 → 使用完后值仍然有效
```

```rust
// Box：存储 trait object
let list: Vec<Box<dyn Animal>> = vec![
    Box::new(Dog {}),
    Box::new(Cat {}),
];

// &：只读引用
fn describe(a: &dyn Animal) -> String {
    a.sound()
}
```

## Q: `Rc<T>` 和 `Arc<T>` 什么时候用？

```rust
// 单线程需要多个所有者 → Rc
let shared: Rc<String> = Rc::new("hello".into());
let a = Rc::clone(&shared);
let b = Rc::clone(&shared);

// 多线程需要多个所有者 → Arc（原子引用计数）
let shared: Arc<String> = Arc::new("hello".into());
let a = Arc::clone(&shared);
let b = Arc::clone(&shared);
```

`RefCell<T>` 在运行时检查借用规则（编译期无法确定）。
