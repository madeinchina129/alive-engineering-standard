# Rust Cargo 配置细则

## 强制规则 (MUST)

### 1. 使用 edition 2021

```toml
# ✅ 正确
[package]
edition = "2021"

# ❌ 错误：使用旧版本
edition = "2018"  # ❌ 缺少新特性支持
```

### 2. 依赖版本精确指定

```toml
# ✅ 正确：明确主版本
serde = { version = "1", features = ["derive"] }
tokio = { version = "1", features = ["rt-multi-thread", "macros"] }

# ❌ 错误：宽松版本或通配
serde = "*"            # ❌ 不锁定版本
tokio = "1"            # ❌ 隐含 full 以外的 feature 可能缺失
```

### 3. features 按功能拆分

```toml
# ✅ 正确：按功能拆分 features
[features]
default = ["std"]
std = []
serde-support = ["serde", "serde_json"]
async = ["tokio", "futures"]

# ❌ 错误：一个 feature 包含所有依赖
[features]
default = ["tokio", "serde", "reqwest", "sqlx"]  # ❌ 无法按需选择
```

### 4. 发布配置优化

```toml
# ✅ 正确：release profile 优化
[profile.release]
opt-level = 3          # 最高优化
lto = true             # 链接时优化
codegen-units = 1      # 单代码生成单元（更优优化）
strip = true           # 去除调试符号（减小体积）

# ❌ 错误：release 用默认配置
# 默认 opt-level=3 但 lto=false, codegen-units=16
```

### 5. 工作空间 workspace 组织多 crate

```toml
# ✅ 正确：workspace 根 Cargo.toml
[workspace]
members = [
    "crates/*",
    "apps/server",
]
resolver = "2"
```

## 推荐实践 (SHOULD)

### dev-dependencies 分离

```toml
[dependencies]  # 应用依赖
serde = "1"
reqwest = "0.12"

[dev-dependencies]  # 仅测试用
criterion = "0.5"
testcontainers = "0"
```

## 禁止行为 (MUST NOT)

- ❌ 使用 `*` 通配版本号
- ❌ prod 依赖中包含 test-only crate（如 criterion）
- ❌ 不指定 edition
- ❌ workspace 中 resolver 使用 `1`（应用用 `2`）
