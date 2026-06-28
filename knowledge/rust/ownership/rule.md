# Rust 所有权与借用细则

## 强制规则 (MUST)

### 1. 优先使用借用而非所有权转移

```rust
// ✅ 正确：使用引用
fn process(data: &[u8]) -> usize {
    data.len()
}

// ❌ 错误：不必要地获取所有权
fn process(data: Vec<u8>) -> usize {
    data.len()  // 调用方失去了 data
}
```

### 2. 可变借用同一时间只能有一个

```rust
// ✅ 正确：可变借用不重叠
let mut s = String::from("hello");
let r1 = &mut s;
r1.push_str(" world");
// r1 的借用结束
let r2 = &mut s;  // ✅ 可以新建可变借用

// ❌ 错误：重叠的可变借用
let mut s = String::from("hello");
let r1 = &mut s;
let r2 = &mut s;  // ❌ 编译错误：不能同时有两个可变引用
r1.push_str(" world");
```

### 3. 不可变借用和可变借用不能共存

```rust
// ✅ 正确：不可变借用使用完后才可变借用
let mut s = String::from("hello");
let r1 = &s;      // 不可变借用
let r2 = &s;      // 不可变借用，允许多个
println!("{r1} {r2}");  // 不可变借用使用完毕
let r3 = &mut s;  // ✅ 可变借用现在可以了

// ❌ 错误：不可变和可变借用共存
let mut s = String::from("hello");
let r1 = &s;
let r3 = &mut s;  // ❌ 编译错误：已有不可变借用
println!("{r1}");
```

### 4. 悬垂引用在编译期被阻止

```rust
// ✅ 正确：返回拥有所有权的值
fn create_string() -> String {
    let s = String::from("hello");
    s  // 所有权转移给调用方
}

// ❌ 错误：返回局部变量的引用
fn create_string() -> &String {
    let s = String::from("hello");
    &s  // ❌ 编译错误：s 离开作用域后被释放
}
```

### 5. 结构体包含引用时必须标注生命周期

```rust
// ✅ 正确：显式生命周期标注
struct Config<'a> {
    host: &'a str,
    port: u16,
}

impl<'a> Config<'a> {
    fn new(host: &'a str, port: u16) -> Self {
        Self { host, port }
    }
}

// ❌ 错误：缺少生命周期标注
struct Config {
    host: &str,  // ❌ 编译错误：缺少生命周期标注
    port: u16,
}
```

### 6. 使用 `&str` 而非 `&String` 作为参数

```rust
// ✅ 正确：接受 &str，更灵活
fn greet(name: &str) {
    println!("Hello, {name}");
}

greet("world");       // ✅ 字面量
greet(&my_string);    // ✅ String 引用自动转为 &str

// ❌ 错误：接受 &String 限制了调用方式
fn greet(name: &String) {
    println!("Hello, {name}");
}
```

## 推荐实践 (SHOULD)

### 1. 需要修改时使用 `&mut self`

```rust
impl Counter {
    // ✅ 修改内部状态
    fn increment(&mut self) {
        self.count += 1;
    }

    // ✅ 只读访问
    fn value(&self) -> u32 {
        self.count
    }
}
```

### 2. 大的数据结构优先使用 Box

```rust
// ✅ 大数据结构放堆上
struct LargeData {
    items: Box<[u8]>,  // 堆分配
}
```

## 禁止行为 (MUST NOT)

- ❌ 同时持有不可变和可变引用
- ❌ 返回局部变量的引用
- ❌ 结构体引用缺少生命周期标注
- ❌ 在不安全代码中手动解引用绕过借用检查
- ❌ `&String` 作为函数参数（应该用 `&str`）
