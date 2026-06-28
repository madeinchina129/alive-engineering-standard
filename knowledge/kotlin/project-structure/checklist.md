# Kotlin 项目结构 Checklist

## 分层架构
- [ ] domain 层是否零框架依赖？
- [ ] 依赖方向是否一致（presentation → application → domain ← infrastructure）？
- [ ] 是否避免循环依赖？

## 文件组织
- [ ] package 是否按层/feature 划分？
- [ ] 是否一个文件一个类（data class 除外）？
- [ ] DTO/值对象是否使用 data class？
- [ ] 文件命名是否和类名一致？

## 依赖注入
- [ ] domain 接口是否在 domain 层定义？
- [ ] 实现类是否在 infrastructure/presentation 层？
- [ ] 是否使用构造函数注入？
