# 组件库标准 — FAQ

## Q1: 组件库的粒度如何划分？
原子组件（Button/Input）→ 分子组件（FormField/SearchBar）→ 有机体（DataTable/Form）→ 模板（PageLayout）。推荐原子和分子组件在组件库中维护，有机体和模板在业务项目中维护。

## Q2: 组件何时需要重构？
当组件 Props 超过 15 个、内部状态逻辑超过 3 个 useState、或文件超过 300 行时，应考虑拆分为子组件。

## Q3: 如何确保组件质量？
每个组件必须包含：单元测试（覆盖率 90%+）、Storybook 用例（覆盖全部 Props 组合）、无障碍评审、视觉回归测试。

## Q4: 组件版本如何管理？
遵循 Semver 规范：破坏性变更（Props 重命名/删除）发 major，新增功能发 minor，Bug 修复发 patch。
