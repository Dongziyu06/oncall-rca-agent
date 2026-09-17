# 部署说明（实验室为主路径）

> **主路径**：实验室 GitLab + 实验室服务器（与 K8s / Prometheus 同网）  
> **可选**：GitHub 公开仓（简历链接）/ 阿里云 ECS（已不推荐，内网数据源连不上）

---

## 仓库与远程

| 远程名 | 地址 | 用途 |
|--------|------|------|
| `origin` | https://github.com/Dongziyu06/oncall-rca-agent.git | 公开 / 简历 |
| `gitlab` | https://gitlab.fir.ac.cn/Dongziyu/oncall-rca-agent.git | CI/CD + 内网部署 |

日常推送：

```powershell
cd D:\aiops\oncall-rca-agent
git push origin main
git push gitlab main
```

---

## 实验室部署（推荐）

### 前置

1. 本机已连 Hillstone VPN  
2. 能 SSH：`ssh cnic@10.10.140.2`  
3. 实验室机已装 Docker + Docker Compose  
4. 服务器上有项目 `.env`（含 `OPENAI_API_KEY`、`PROMETHEUS_URL`、`KUBECONFIG` 等）

### 首次安装（在实验室机上执行一次）

```bash
ssh cnic@10.10.140.2

# 选一个有写权限的目录，例如家目录
cd ~
git clone https://gitlab.fir.ac.cn/Dongziyu/oncall-rca-agent.git
cd oncall-rca-agent
cp .env.example .env
nano .env   # 填写 LLM Key；K8s/Prometheus 指向本机或内网地址
# 例：
# PROMETHEUS_URL=http://10.10.140.2:30090
# KUBECONFIG=/home/cnic/.kube/config
# K8S_VERIFY_SSL=false

docker compose up -d --build
curl http://127.0.0.1:8000/health
```

演示（VPN 下）：http://10.10.140.2:8000  

也可用脚本：

```bash
export DEPLOY_PATH=$HOME/oncall-rca-agent
bash scripts/deploy_lab.sh
```

### 手动更新

```bash
ssh cnic@10.10.140.2
cd ~/oncall-rca-agent   # 或你的 DEPLOY_PATH
git pull
docker compose up -d --build
docker compose logs --tail=50
```

---

## GitLab CI/CD

流水线文件：`.gitlab-ci.yml`

| 作业 | 触发 | 作用 |
|------|------|------|
| `test` | 每次 push / MR | `pytest` |
| `deploy_lab` | 仅 `main`，**手动**点 Play | SSH 到实验室机执行 `scripts/deploy_lab.sh` |

### 配置 CI 变量

GitLab → **Settings → CI/CD → Variables**：

| 变量 | 示例 | 说明 |
|------|------|------|
| `LAB_HOST` | `10.10.140.2` | 部署机 |
| `LAB_USER` | `cnic` | SSH 用户 |
| `LAB_SSH_PRIVATE_KEY` | 私钥全文 | 建议 Type=File；Protected |
| `LAB_DEPLOY_PATH` | `/home/cnic/oncall-rca-agent` | 与首次克隆路径一致 |

本机生成部署密钥（示例）：

```bash
ssh-keygen -t ed25519 -C "gitlab-deploy" -f deploy_lab -N ""
# 把 deploy_lab.pub 追加到实验室机 ~/.ssh/authorized_keys
# 把 deploy_lab 私钥内容贴进 LAB_SSH_PRIVATE_KEY
```

### 若没有可用 Runner

到 **Settings → CI/CD → Runners** 看是否有 Shared / Group / Project Runner。  
没有则：

1. 请管理员开通 Shared Runner，或  
2. 在实验室机注册 Shell/Docker Runner（打 tag `lab`），或  
3. 暂时只用「手动 SSH + `deploy_lab.sh`」，CI 只跑 `test`（无 Runner 时连 test 也不会跑）

### 可选：Runner 就在实验室机上

把 `.gitlab-ci.yml` 里 `deploy_lab_shell` 注释打开，Runner tag 设为 `lab`，即可 `git push` 后自动本机部署，无需 SSH 变量。

---

## 阿里云 ECS（可选 / 不推荐作主演示）

| 项 | 值 |
|----|-----|
| 公网 | http://123.56.47.94:8000 |
| SSH | `ssh root@123.56.47.94` |
| 路径 | `/opt/oncall-rca-agent` |

ECS **默认访问不到** 实验室 K8s/Prometheus，真实取证演示请用实验室部署。  
省钱：可停机或到期不续。

---

## 回滚

```bash
cd $DEPLOY_PATH
git log --oneline -5
git reset --hard <commit>
docker compose up -d --build
```

---

## 常见问题

| 现象 | 处理 |
|------|------|
| 页面打不开 | VPN 是否连上；`docker compose ps`；端口 8000 |
| LLM 不工作 | 服务器 `.env` 的 `OPENAI_API_KEY` / `OPENAI_BASE_URL` |
| K8s 仍 mock | `KUBECONFIG` 路径、`K8S_VERIFY_SSL=false`、VPN |
| CI deploy 失败 | 检查 Variables、公钥是否进 authorized_keys、路径是否存在 |
| git pull 要密码 | 在服务器配 GitLab Deploy Token / SSH deploy key |
