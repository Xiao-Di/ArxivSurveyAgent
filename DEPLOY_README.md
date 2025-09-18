# 🚀 AI文献综述系统 - 部署指南 (v1.1)

本文档详细介绍了如何部署 PaperSurveyAgent AI文献综述系统 v1.1，让其他用户可以访问和使用。

## 📋 部署概览

PaperSurveyAgent v1.1 是一个功能完整的AI文献综述系统，支持多种部署方式：

1. **本地Docker部署** - 适合个人开发测试
2. **服务器部署** - 适合小团队使用
3. **域名部署** - 适合生产环境
4. **云平台部署** - 适合大规模使用

### 🌟 v1.1 新特性
- **用户系统**: 完整的注册、登录、认证流程
- **支付功能**: 余额管理和支付宝充值集成
- **智能定价**: 0.1元/篇论文，最低消费0.5元
- **错误处理**: 详细的余额不足提示和充值引导
- **数据持久化**: SQLite数据库存储用户和支付记录

## 🔧 环境要求

### 基础环境
- **操作系统**: Linux (推荐 Ubuntu 20.04+)
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Python**: 3.9+ (本地开发)
- **Node.js**: 18+ (前端开发)
- **内存**: 至少 4GB RAM
- **存储**: 至少 10GB 可用空间

### API密钥要求
- **DeepSeek API Key** (必需) - [获取地址](https://platform.deepseek.com/)
- **OpenAI API Key** (可选) - 用于 embeddings
- **Semantic Scholar API Key** (可选)

## 🏠 方案1：本地Docker部署（推荐用于个人使用）

### 快速启动
```bash
# 1. 进入项目目录
cd AI-Agent-for-Automated-Literature-Review-Summarization

# 2. 配置API密钥
cp config/config.example.env config/.env
# 编辑 config/.env 文件，设置你的DEEPSEEK_API_KEY

# 3. 一键启动
python scripts/quick_start.py

# 4. 访问应用
# 前端界面: http://localhost:5174
# 后端API: http://localhost:8000
# API文档: http://localhost:8000/docs
```

### 管理命令
```bash
# 查看服务状态
docker-compose ps

# 查看日志
python scripts/quick_start.py --logs

# 停止服务
python scripts/quick_start.py --stop

# 重新构建并启动
python scripts/quick_start.py --build

# 清理所有容器和镜像
python scripts/quick_start.py --clean
```

## 🌐 方案2：服务器部署（让其他人访问）

### 2.1 准备服务器
推荐云服务提供商：
- **阿里云ECS**: 性价比高，国内访问快
- **腾讯云CVM**: 价格优惠，学生优惠多
- **AWS EC2**: 全球覆盖，功能完善
- **Google Cloud**: 技术领先，免费额度多

### 2.2 服务器初始化
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 添加用户到docker组
sudo usermod -aG docker $USER
newgrp docker

# 验证安装
docker --version
docker-compose --version
```

### 2.3 部署应用
```bash
# 1. 克隆项目
git clone <你的GitHub仓库地址>
cd AI-Agent-for-Automated-Literature-Review-Summarization

# 2. 配置环境
cp config/config.example.env config/.env
# 编辑config/.env文件，设置API密钥

# 3. 启动服务
python scripts/quick_start.py --prod

# 4. 开放防火墙端口
sudo ufw allow 8000    # 后端API
sudo ufw allow 5174    # 前端界面
sudo ufw allow 22      # SSH
sudo ufw enable

# 5. 检查服务状态
curl http://localhost:8000/api/health
```

### 2.4 用户访问方式
- **HTTP访问**: http://服务器IP:5174
- **API访问**: http://服务器IP:8000
- **API文档**: http://服务器IP:8000/docs

## 🌍 方案3：域名部署（专业级）

### 3.1 准备工作
1. **购买域名**
   - 阿里云域名：[wanwang.aliyun.com](https://wanwang.aliyun.com)
   - 腾讯云域名：[cloud.tencent.com](https://cloud.tencent.com)
   - NameSilo：[namesilo.com](https://www.namesilo.com)
   - Cloudflare：[cloudflare.com](https://www.cloudflare.com)

2. **域名解析**
   - A记录：域名 → 服务器IP
   - WWW记录：www.域名 → 服务器IP

### 3.2 使用部署脚本
```bash
# 1. 修改部署脚本配置
nano scripts/deploy.sh
# 修改 DOMAIN 和 EMAIL 变量

# 2. 设置执行权限
chmod +x scripts/deploy.sh

# 3. 运行部署脚本
sudo ./scripts/deploy.sh

# 4. 按照提示输入域名和邮箱
```

### 3.3 手动部署步骤
```bash
# 1. 创建必要目录
sudo mkdir -p /opt/literature-review/{data,logs,nginx/ssl}
sudo chown -R $USER:$USER /opt/literature-review

# 2. 复制项目文件
cp -r ./* /opt/literature-review/
cd /opt/literature-review

# 3. 配置SSL证书
sudo apt install certbot -y
sudo certbot certonly --standalone --email your-email@example.com \
    --agree-tos --no-eff-email -d your-domain.com -d www.your-domain.com

# 4. 复制证书
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/key.pem

# 5. 修改nginx配置
sed -i 's/your-domain.com/your-domain.com/g' nginx/nginx.conf

# 6. 启动服务
docker-compose -f docker-compose.prod.yml up -d

# 7. 设置证书自动续期
(crontab -l 2>/dev/null; echo "0 2 * * * certbot renew --quiet") | crontab -
```

### 3.4 访问测试
```bash
# 检查HTTPS访问
curl -I https://your-domain.com

# 检查API服务
curl https://your-domain.com/api/health

# 检查前端
curl https://your-domain.com/
```

## ☁️ 方案4：云平台一键部署

### 4.1 Docker Cloud部署
```bash
# 使用Docker Compose生产配置
docker-compose -f docker-compose.prod.yml up -d

# 查看服务状态
docker-compose -f docker-compose.prod.yml ps

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f
```

### 4.2 Kubernetes部署
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: literature-review-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: literature-review
  template:
    metadata:
      labels:
        app: literature-review
    spec:
      containers:
      - name: app
        image: literature-review:latest
        ports:
        - containerPort: 8000
        env:
        - name: DEEPSEEK_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: deepseek-api-key
```

### 4.3 云服务商特有部署
- **阿里云ACK**: 使用容器服务Kubernetes版
- **腾讯云TKE**: 使用弹性容器服务
- **AWS EKS**: 使用Elastic Kubernetes Service
- **Google GKE**: 使用Google Kubernetes Engine

## 🔍 部署后验证

### 服务健康检查
```bash
# 检查后端API
curl http://localhost:8000/api/health

# 检查API文档
curl http://localhost:8000/docs

# 检查前端页面
curl -I http://localhost:5174

# 检查数据库连接
docker-compose exec redis redis-cli ping
```

### 功能测试
1. **用户注册测试**
   - 访问前端界面
   - 点击"注册"按钮
   - 填写注册信息
   - 验证注册成功

2. **用户登录测试**
   - 使用注册的账号登录
   - 验证登录状态显示
   - 测试搜索功能

3. **搜索功能测试**
   - 输入搜索关键词
   - 验证搜索结果
   - 测试报告生成

## 🛠️ 常见问题解决

### 问题1：端口被占用
```bash
# 查看端口占用
lsof -i :8000
netstat -tulpn | grep :8000

# 修改端口
# 编辑 docker-compose.yml，修改端口映射
ports:
  - "8001:8000"  # 改为其他端口
```

### 问题2：API密钥错误
```bash
# 检查环境变量
docker-compose exec literature-review-app env | grep DEEPSEEK

# 重新配置密钥
# 编辑 config/.env 文件
# 重启服务
docker-compose restart literature-review-app
```

### 问题3：Docker构建失败
```bash
# 清理Docker缓存
docker system prune -a

# 重新构建
docker-compose build --no-cache

# 查看构建日志
docker-compose build --no-cache --progress=plain
```

### 问题4：用户无法注册
```bash
# 检查数据库
docker-compose exec literature-review-app ls -la /app/data/

# 检查权限
docker-compose exec literature-review-app chmod 755 /app/data/

# 重启服务
docker-compose restart literature-review-app
```

## 🔧 配置文件说明

### 环境变量配置
```bash
# config/.env
# DeepSeek API配置
DEEPSEEK_API_KEY=your-api-key-here
DEEPSEEK_MODEL=deepseek-reasoner
DEEPSEEK_API_BASE=https://api.deepseek.com/v1

# 可选配置
OPENAI_API_KEY=your-openai-key
SEMANTIC_SCHOLAR_API_KEY=your-semantic-key

# 应用配置
LOG_LEVEL=INFO
DEBUG=false
UVICORN_WORKERS=2

# JWT配置
JWT_SECRET_KEY=your-jwt-secret-key
```

### Docker Compose配置
```yaml
# 生产环境优化
environment:
  - UVICORN_WORKERS=2  # 增加工作进程数
  - REDIS_MAXMEMORY=512mb  # 增加Redis内存
volumes:
  - ./data:/app/data  # 持久化数据
  - ./logs:/app/logs  # 日志文件
restart_policy: unless-stopped  # 自动重启
```

## 📊 性能优化

### 服务器配置建议
- **CPU**: 2核心以上
- **内存**: 4GB以上
- **存储**: SSD硬盘，50GB以上
- **网络**: 10Mbps以上带宽

### 优化设置
```yaml
# docker-compose.prod.yml
environment:
  - UVICORN_WORKERS=4  # 4核CPU建议
  - REDIS_MAXMEMORY=1gb  # 增加缓存
  - CHROMA_PERSIST_DIRECTORY=/app/data/chroma_db
```

## 🔒 安全配置

### 基础安全措施
1. **防火墙配置**
```bash
# 只开放必要端口
sudo ufw allow 22      # SSH
sudo ufw allow 80      # HTTP
sudo ufw allow 443     # HTTPS
sudo ufw deny from any to any  # 默认拒绝
```

2. **SSL证书**
```bash
# 使用Let's Encrypt免费证书
sudo certbot renew --dry-run  # 测试续期
sudo certbot certificates     # 查看证书
```

3. **定期备份**
```bash
# 备份脚本
#!/bin/bash
tar -czf backup-$(date +%Y%m%d).tar.gz data/ config/
# 设置定时任务
0 2 * * * /path/to/backup.sh
```

## 📈 监控和维护

### 系统监控
```bash
# 查看资源使用
docker stats

# 查看日志
docker-compose logs -f --tail=100

# 健康检查
curl http://localhost:8000/api/health
```

### 日志管理
```bash
# 日志轮转配置
# /etc/logrotate.d/literature-review
/opt/literature-review/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 root root
}
```

---

## 🤝 技术支持

如果部署过程中遇到问题：

1. **查看日志**: `docker-compose logs -f`
2. **检查文档**: [API文档](http://localhost:8000/docs)
3. **健康检查**: `curl http://localhost:8000/api/health`
4. **GitHub Issues**: [提交问题](https://github.com/yourusername/tsearch/issues)

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。