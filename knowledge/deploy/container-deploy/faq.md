# 容器化部署规范 — FAQ

## Q1: Alpine vs Distroless vs Ubuntu？
Distroless（推荐）：只包含应用及其运行时依赖，无 shell/包管理器，攻击面最小。Alpine：体积小（5MB）、有包管理器、但 musl libc 可能导致兼容性问题。Ubuntu：最兼容、体积大、安全更新频繁。

## Q2: 镜像体积应该多大？
编译型语言（Go/Rust）目标 < 20MB，解释型语言（Python/Node）目标 < 200MB。超过 1GB 的镜像说明需要优化依赖管理或使用基础镜像。
