#!/usr/bin/env bash
# 实验室部署脚本：可被 GitLab CI SSH 调用，也可在服务器上手动执行
# 用法：
#   export DEPLOY_PATH=/opt/oncall-rca-agent   # 可选
#   bash scripts/deploy_lab.sh
set -euo pipefail

DEPLOY_PATH="${DEPLOY_PATH:-/opt/oncall-rca-agent}"
GITLAB_URL="${GITLAB_URL:-https://gitlab.fir.ac.cn/Dongziyu/oncall-rca-agent.git}"

echo "==> deploy path: ${DEPLOY_PATH}"
echo "==> commit: ${CI_COMMIT_SHA:-manual}"

if [ ! -d "${DEPLOY_PATH}/.git" ]; then
  echo "==> 首次克隆仓库到 ${DEPLOY_PATH}"
  sudo mkdir -p "$(dirname "${DEPLOY_PATH}")" 2>/dev/null || mkdir -p "$(dirname "${DEPLOY_PATH}")"
  git clone "${GITLAB_URL}" "${DEPLOY_PATH}"
fi

cd "${DEPLOY_PATH}"

# 确保远程指向实验室 GitLab
if git remote get-url gitlab >/dev/null 2>&1; then
  git fetch gitlab
  git checkout main
  git reset --hard gitlab/main
elif git remote get-url origin >/dev/null 2>&1; then
  # 若 origin 已是 GitLab，直接 pull
  git fetch origin
  git checkout main
  git reset --hard origin/main
else
  git remote add gitlab "${GITLAB_URL}"
  git fetch gitlab
  git checkout -B main gitlab/main
fi

if [ ! -f .env ]; then
  echo "==> 缺少 .env，从 .env.example 复制（请稍后填入 LLM Key / KUBECONFIG）"
  cp .env.example .env
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: 未安装 docker，请先在实验室机安装 Docker + Compose"
  exit 1
fi

echo "==> docker compose up -d --build"
docker compose up -d --build
docker compose ps

echo "==> health check"
sleep 3
curl -fsS "http://127.0.0.1:8000/health" || true
echo
echo "==> deploy done. 演示（需 VPN）: http://10.10.140.2:8000"
