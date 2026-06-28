# Rust Cargo Checklist

## package
- [ ] `edition` 是否设置为 `2021`？
- [ ] `version` 是否遵循语义化版本？
- [ ] `description` 是否有意义？
- [ ] `license` 是否指定？

## dependencies
- [ ] 版本号是否精确（无 `*`）？
- [ ] 是否使用 `features` 按需选择依赖功能？
- [ ] 仅测试用的依赖是否在 `[dev-dependencies]`？
- [ ] 构建工具是否在 `[build-dependencies]`？

## features
- [ ] 是否按功能拆分 features？
- [ ] `default` features 是否最小化？
- [ ] 可选依赖是否用 `dep:` 语法？
- [ ] features 是否有文档说明？

## profile
- [ ] `[profile.release]` 是否配置了 `lto = true`？
- [ ] 是否配置了 `strip = true`（减小体积）？
- [ ] `codegen-units` 是否为 `1`（发布版）？

## workspace
- [ ] 多 crate 是否使用 workspace？
- [ ] `resolver` 是否设为 `2`？
- [ ] workspace 成员是否有明确的目录结构？
