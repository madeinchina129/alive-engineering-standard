```dockerfile
# Dockerfile - Python Web 应用

# === Builder Stage ===
FROM python:3.12-slim AS builder

WORKDIR /app

# 只复制依赖文件，利用缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# === Runner Stage ===
FROM python:3.12-slim AS runner

# 安全配置：非 root 用户
RUN groupadd -r app && useradd -r -g app -d /app -s /sbin/nologin app

# 只复制必要文件
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY ./src /app/src

WORKDIR /app
USER app

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# .dockerignore
# __pycache__/
# .git/
# .env
# tests/
# *.md

# 构建命令
# docker build -t myapp:latest .
# docker run -d -p 8000:8000 --memory=512m --cpus=1 myapp:latest

# 镜像安全扫描
# trivy image myapp:latest
```