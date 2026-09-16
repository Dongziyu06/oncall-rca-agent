"""
端到端一键测试脚本 - 单窗口全自动
用法：
  python test_e2e.py           # 运行全部场景
  python test_e2e.py --restart # 强制重启服务再测试
  python test_e2e.py --one     # 只跑第 1 个场景（快速验证）
"""
import subprocess, sys, time, httpx, json, os, atexit, threading

BASE = "http://127.0.0.1:8000"
SERVER_PROC = None
LOG_LINES = []

# ── 工具：杀掉占用 8000 端口的进程 ─────────────────────────────────
def kill_port_8000():
    try:
        out = subprocess.check_output("netstat -aon", shell=True, text=True, errors="ignore")
        for line in out.splitlines():
            if ":8000 " in line or ":8000\t" in line:
                parts = line.strip().split()
                pid = parts[-1]
                if pid.isdigit() and pid != "0":
                    subprocess.call(f"taskkill /F /PID {pid}", shell=True,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

# ── 检查服务是否在线 ─────────────────────────────────────────────
def server_up() -> bool:
    try:
        return httpx.get(f"{BASE}/docs", timeout=2).status_code == 200
    except Exception:
        return False

# ── 启动 uvicorn，日志同时打印到终端 ────────────────────────────────
def start_server():
    global SERVER_PROC
    kill_port_8000()
    time.sleep(0.5)
    print("🚀 启动服务中 ...", flush=True)

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"

    SERVER_PROC = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.main:app",
         "--port", "8000", "--log-level", "warning"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace",
        cwd=os.path.dirname(os.path.abspath(__file__)),
        env=env,
    )
    atexit.register(lambda: SERVER_PROC.terminate())

    # 后台线程实时打印服务日志（只打印 DEBUG/WARNING/ERROR 行）
    def _tail():
        for line in SERVER_PROC.stdout:
            line = line.rstrip()
            LOG_LINES.append(line)
            if any(k in line for k in ["DEBUG", "ERROR", "error", "Error", "WARNING", "WARN"]):
                print(f"  [srv] {line}", flush=True)
    threading.Thread(target=_tail, daemon=True).start()

    for _ in range(30):
        time.sleep(0.5)
        if server_up():
            print("✅ 服务就绪\n", flush=True)
            return
    print("❌ 服务启动超时，请检查上方日志")
    sys.exit(1)

# ── 决定是否需要（重）启动 ────────────────────────────────────────
if "--restart" in sys.argv or not server_up():
    start_server()
else:
    print("✅ 服务已在运行（加 --restart 可强制重启）\n")

# ── 测试场景 ─────────────────────────────────────────────────────
SCENARIOS = [
    {
        "name": "CPU 高负载",
        "payload": {"alerts": [{"labels": {"alertname": "HighCPU", "service": "demo"},
                                 "annotations": {"description": "CPU usage above 90% for 10 minutes"}}]},
    },
    {
        "name": "OOM 内存溢出",
        "payload": {"alerts": [{"labels": {"alertname": "OOMKilled", "service": "payment"},
                                 "annotations": {"description": "Container OOM killed, exit code 137"}}]},
    },
    {
        "name": "Pod CrashLoop",
        "payload": {"alerts": [{"labels": {"alertname": "PodCrashLooping", "service": "api-server"},
                                 "annotations": {"description": "Pod restarting repeatedly, CrashLoopBackOff"}}]},
    },
]

if "--one" in sys.argv:
    SCENARIOS = SCENARIOS[:1]

# ── 运行 ─────────────────────────────────────────────────────────
with httpx.Client(timeout=90) as c:
    for i, sc in enumerate(SCENARIOS, 1):
        print(f"{'='*62}")
        print(f"  【场景 {i}/{len(SCENARIOS)}】{sc['name']}")
        print(f"{'='*62}")

        r = c.post(f"{BASE}/alert", json=sc["payload"])
        task_id = r.json()["task_id"]
        print(f"  task_id: {task_id}\n")

        report_text = ""
        with c.stream("GET", f"{BASE}/task/{task_id}/stream") as stream:
            for line in stream.iter_lines():
                if not line.startswith("data:"):
                    continue
                data = json.loads(line[5:].strip())

                if data["type"] == "progress":
                    node, status = data["node"], data["status"]
                    result = data.get("result", "")
                    if status == "started":
                        print(f"  ⏳ {node:<14}", end="", flush=True)
                    elif status == "completed":
                        extra = f" → {result}" if result else ""
                        print(f"\r  ✅ {node:<14}{extra}")

                elif data["type"] == "report":
                    report_text = data["report"]

        is_template = "置信度**：0.72" in report_text or "Confidence**: 0.72" in report_text or ("0.72" in report_text and "核对指标" in report_text)
        llm_tag = "⚠️  [模板回退]" if is_template else "🤖 [LLM生成]"
        print(f"\n  {llm_tag} 报告如下：")
        print("─" * 62)
        print(report_text)
        print()
        time.sleep(1)

print("🏁 全部场景完成")
