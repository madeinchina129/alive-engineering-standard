# Rust Cargo 配置规范

## Cargo.toml 结构

```toml
[package]
name = "myapp"
version = "0.1.0"
edition = "2021"
description = "一个 Rust 应用"
authors = ["Team"]
license = "MIT"

[dependencies]
serde = { version = "1", features = ["derive"] }
tokio = { version = "1", features = ["full"] }

[dev-dependencies]
criterion = "0.5"

[build-dependencies]
tonic-build = "0.12"

[features]
default = ["std"]
std = []

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
```

---

## 关键配置项

| 配置 | 说明 | 推荐值 |
|------|------|--------|
| `edition` | 语言版本 | `2021` |
| `[dependencies]` | 运行时依赖 | 精确版本号 |
| `[dev-dependencies]` | 测试/bench 依赖 | 放这里 |
| `[features]` | 特性门控 | 按功能拆分 |
| `[profile.release]` | 发布配置 | opt-level=3, lto=true |
| `[workspace]` | 多 crate 工作空间 | 组织多模块 |

---

## 适用范围

- **所有 Rust 项目**：严格遵循 Cargo 配置规范
- **CLI 工具**：`[dependencies]` 最小化
- **库 crate**：`edition 2021` + 语义化版本
