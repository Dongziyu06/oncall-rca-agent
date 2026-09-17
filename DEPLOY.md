# 服务器更新清单（无 CI/CD 时）

演示地址：http://123.56.47.94:8000  
服务器路径：`/opt/oncall-rca-agent`  
仓库：https://github.com/Dongziyu06/oncall-rca-agent

当前云上能力：告警 RCA 流水线、对话分析（`/chat`）、MCP（`/mcp`）、Web UI。  
服务器 `.env` 需自行配置 LLM Key；实验室 K8s/Prometheus 仅本机 VPN 可达，**ECS 默认连不上实验室内网**，云上演示走 mock 或公网数据源。

---

## 日常更新（改完代码后）

### 本机（Windows）

```cmd
cd d:\aiops\oncall-rca-agent
git add .
git commit -m "说明这次改了什么"
git push origin main
```

### 服务器（SSH 登录后）

```bash
ssh root@123.56.47.94

cd /opt/oncall-rca-agent
git pull origin main
docker compose up -d --build
docker compose ps
docker compose logs --tail=50
```

浏览器强制刷新：`http://123.56.47.94:8000`

---

## 只改了前端 / 文档（未改依赖）

有时不必全量 rebuild（仍建议稳妥用上面的 `up -d --build`）。  
若确认只改了静态文件且镜像里已 COPY 最新代码，仍以 `build` 为准最不容易错。

---

## 只改了 `.env`（密钥 / 模型 / 地址）

`.env` 不在 Git 里，必须在**服务器上**改：

```bash
cd /opt/oncall-rca-agent
nano .env
docker compose up -d
```

---

## 回滚到上一版

```bash
cd /opt/oncall-rca-agent
git log --oneline -5
git checkout <上一个commit>
docker compose up -d --build
```

恢复最新：

```bash
git checkout main
git pull
docker compose up -d --build
```

---

## 常见检查

| 现象 | 检查命令 |
|------|----------|
| 页面打不开 | `docker compose ps`；安全组是否放行 8000 |
| 容器反复重启 | `docker compose logs --tail=100` |
| LLM 不工作 | 服务器 `.env` 里 `OPENAI_API_KEY` 是否填对 |
| git pull 失败 | 网络/GitHub；可改用代理或本机 `scp` 上传 |

---

## 账号速查（无密钥）

| 项 | 值 |
|----|-----|
| GitHub | `Dongziyu06/oncall-rca-agent` |
| 公网 IP | `123.56.47.94` |
| SSH | `ssh root@123.56.47.94` |
| 演示 URL | http://123.56.47.94:8000 |
