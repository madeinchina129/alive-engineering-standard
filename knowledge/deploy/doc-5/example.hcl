```hcl
# Terraform 环境配置示例
# environments/production/main.tf

terraform {
  backend "s3" {
    bucket = "company-terraform-state"
    key    = "production/terraform.tfstate"
    region = "us-east-1"
  }
}

module "app_infrastructure" {
  source = "../../modules/app"

  environment = "production"
  region      = "us-east-1"
  
  # 生产环境配置
  instance_count = 5
  instance_type  = "t3.large"
  min_capacity   = 3
  max_capacity   = 20
  
  # 数据库
  db_instance_class  = "db.r6g.large"
  db_multi_az       = true
  db_backup_retention = 30
  
  # 监控
  alert_severity_thresholds = {
    p0 = "5m"
    p1 = "30m"
    p2 = "8h"
  }
  
  # 日志
  log_retention_days = 90
  
  # 安全
  enable_waf         = true
  enable_ddos_protection = true
  allowed_cidr_blocks = ["10.0.0.0/8"]
}

# 环境的差异点（相比 Staging）
# - 实例规格更大 (t3.large vs t3.medium)
# - 多可用区部署 (multi_az=true)
# - 备份保留更长 (30天 vs 7天)
# - 日志保留更长 (90天 vs 30天)
# - 启用 WAF 和 DDoS 防护
# - 数据库 Multi-AZ

# 环境入口/出口标准
# Dev: 代码在本地可运行 → 提交 PR
# Test: CI 通过 + Code Review 通过 → 合并到主分支
# Staging: 集成测试通过 + 性能测试通过 → 批准发布
# Production: Staging 验证通过 + 变更审批 → 上线
```