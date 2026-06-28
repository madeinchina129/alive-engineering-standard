```bash
#!/bin/bash
# MySQL 自动备份脚本

# 配置
DB_HOST="localhost"
DB_USER="backup_user"
DB_NAME="production_db"
BACKUP_DIR="/data/backup/mysql"
DATE=$(date +%Y%m%d)
RETENTION_DAYS=30

# 全量备份（每周末）
if [ $(date +%u) -eq 7 ]; then
    mysqldump -h $DB_HOST -u $DB_USER \
        --single-transaction --quick --routines --triggers \
        $DB_NAME | gzip > $BACKUP_DIR/full/$DB_NAME-$DATE.sql.gz
    
    # 生成 checksum
    md5sum $BACKUP_DIR/full/$DB_NAME-$DATE.sql.gz > $BACKUP_DIR/full/$DB_NAME-$DATE.sql.gz.md5
fi

# 增量备份（binlog）
mysqlbinlog -h $DB_HOST -u $DB_USER \
    --read-from-remote-server --to-last-log \
    --result-file=$BACKUP_DIR/binlog/$DB_NAME-$DATE-binlog.sql

# 清理过期备份
find $BACKUP_DIR/full -name "*.gz" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR/full -name "*.md5" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR/binlog -name "*.sql" -mtime +$RETENTION_DAYS -delete

# 加密备份文件（传输到异地）
gpg --encrypt --recipient backup@company.com \
    $BACKUP_DIR/full/$DB_NAME-$DATE.sql.gz
scp $BACKUP_DIR/full/$DB_NAME-$DATE.sql.gz.gpg backup@remote:/data/backup/
```