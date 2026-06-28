# Rust Cargo FAQ

## Q: `edition` 选哪个？

2021 是目前最新稳定 edition，支持：
- 闭包捕获改进
- `prelude` 更新
- `IntoIterator` for arrays
- `const` 泛型基础支持

## Q: `features` 怎么设计？

```toml
[features]
default = ["std"]        # 默认开启的功能
std = []                 # 基础功能（无额外依赖）
serde = ["dep:serde"]    # 可选序列化
```

原则：每个 feature 代表一个可选的独立功能，不耦合。

## Q: `[profile.release]` 配置对二进制大小的影响？

```toml
opt-level = "z"   # 最小体积（-Oz）
lto = true        # 链接时优化，减少体积
strip = true      # 去除调试符号
codegen-units = 1 # 更优优化但编译更慢
```

## Q: workspace 和单个 crate 怎么选？

```
单个 crate：简单项目
workspace：多模块、共享依赖、微服务
```

```toml
# workspace 根
[workspace]
members = ["crates/*", "apps/*"]
resolver = "2"
```

## Q: `[dependencies]` 和 `[dev-dependencies]` 的区别？

```
[dependencies] → 编译进生产二进制
[dev-dependencies] → 仅测试和 bench，不编译进 release
```

`criterion`、`testcontainers`、`rstest` 等测试工具放在 dev-dependencies。
