from dotenv import load_dotenv
load_dotenv()  # 最先加载 .env，确保所有模块都能读到环境变量

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from api.routes.alert import router as alert_router
from api.routes.task import router as task_router
from api.routes.chat import router as chat_router

_mcp_app = None
try:
    from tools.mcp_server import mcp
    _mcp_app = mcp.streamable_http_app()
except Exception as exc:
    print(f"[MCP WARNING] MCP server unavailable: {exc}", flush=True)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # FastAPI 不会自动跑子应用 lifespan，必须在这里启动 MCP session manager
    if _mcp_app is not None:
        async with mcp.session_manager.run():
            yield
    else:
        yield


app = FastAPI(title='OnCall RCA Agent', version='0.3.0', lifespan=lifespan)
app.include_router(alert_router)
app.include_router(task_router)
app.include_router(chat_router)


@app.api_route('/mcp', methods=['GET', 'POST', 'DELETE'], include_in_schema=False)
async def mcp_redirect(request: Request):
    qs = f'?{request.url.query}' if request.url.query else ''
    return RedirectResponse(url=f'/mcp/{qs}', status_code=307)


if _mcp_app is not None:
    app.mount('/mcp', _mcp_app)


@app.get('/health')
async def health():
    return {'status': 'ok'}


app.mount('/', StaticFiles(directory='static', html=True), name='static')
