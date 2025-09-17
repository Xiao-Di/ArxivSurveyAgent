#!/bin/bash

# AI文献综述系统 - 部署脚本
# 用于在生产环境中部署应用

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置变量
DOMAIN="your-domain.com"  # 替换为你的域名
EMAIL="your-email@example.com"  # 替换为你的邮箱

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否为root用户
if [[ $EUID -ne 0 ]]; then
   log_error "此脚本需要root权限运行"
   exit 1
fi

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    log_error "Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    log_error "Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

log_info "开始部署AI文献综述系统..."

# 创建必要目录
log_info "创建必要目录..."
mkdir -p /opt/literature-review
mkdir -p /opt/literature-review/data
mkdir -p /opt/literature-review/logs
mkdir -p /opt/literature-review/ssl
mkdir -p /opt/literature-review/nginx/ssl

# 复制项目文件
log_info "复制项目文件..."
cp -r ./* /opt/literature-review/
cd /opt/literature-review

# 设置权限
chown -R 1000:1000 /opt/literature-review
chmod -R 755 /opt/literature-review

# 生成SSL证书（使用Let's Encrypt）
log_info "生成SSL证书..."
if [ ! -f "/opt/literature-review/nginx/ssl/cert.pem" ]; then
    # 安装certbot
    apt update
    apt install -y certbot

    # 停止nginx（如果运行）
    docker-compose down nginx 2>/dev/null || true

    # 获取证书
    certbot certonly --standalone --email $EMAIL --agree-tos --no-eff-email -d $DOMAIN -d www.$DOMAIN

    # 复制证书
    cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem /opt/literature-review/nginx/ssl/cert.pem
    cp /etc/letsencrypt/live/$DOMAIN/privkey.pem /opt/literature-review/nginx/ssl/key.pem

    # 设置证书权限
    chmod 600 /opt/literature-review/nginx/ssl/*.pem
fi

# 替换域名配置
log_info "配置域名..."
sed -i "s/your-domain.com/$DOMAIN/g" nginx/nginx.conf

# 创建环境变量文件
log_info "配置环境变量..."
if [ ! -f "config/.env" ]; then
    cp config/config.example.env config/.env
    log_warn "请编辑 config/.env 文件并设置你的API密钥"
    log_warn "特别是 DEEPSEEK_API_KEY 变量"
fi

# 构建并启动服务
log_info "构建Docker镜像..."
docker-compose build --no-cache

log_info "启动服务..."
docker-compose up -d

# 等待服务启动
log_info "等待服务启动..."
sleep 30

# 检查服务状态
log_info "检查服务状态..."
if curl -f https://$DOMAIN/health > /dev/null 2>&1; then
    log_info "服务启动成功！"
    log_info "访问地址："
    log_info "  - 主页: https://$DOMAIN"
    log_info "  - API文档: https://$DOMAIN/docs"
    log_info "  - 健康检查: https://$DOMAIN/health"
else
    log_error "服务启动失败，请检查日志："
    docker-compose logs
    exit 1
fi

# 设置自动续期SSL证书
log_info "设置SSL证书自动续期..."
(crontab -l 2>/dev/null; echo "0 2 * * * certbot renew --quiet --post-hook 'docker-compose exec nginx nginx -s reload'") | crontab -

log_info "部署完成！"
log_info "管理命令："
log_info "  - 查看日志: docker-compose logs -f"
log_info "  - 停止服务: docker-compose down"
log_info "  - 重启服务: docker-compose restart"