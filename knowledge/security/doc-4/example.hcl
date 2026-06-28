```hcl
# HashiCorp Vault 策略示例
# 密钥管理策略
path "secret/data/production/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
  required_parameters = ["data"]
  
  # 生产环境密钥仅允许运维团队写入
  constraint {
    path "secret/data/production/db/*" {
      capabilities = ["read"]
    }
    path "secret/data/production/api/*" {
      capabilities = ["read"]
    }
  }
}

# 密钥轮换配置
path "sys/rotate" {
  capabilities = ["sudo"]
}

# 审计日志
path "audit/*" {
  capabilities = ["read", "list"]
}
```