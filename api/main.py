from dotenv import load_dotenv
load_dotenv()  # 最先加载 .env，确保所有模块都能读到环境变量

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routes.alert import router as alert_router
from api.routes.task import router as task_router
app=FastAPI(title='OnCall RCA Agent',version='0.3.0')
app.include_router(alert_router); app.include_router(task_router)
@app.get('/health')
async def health(): return {'status':'ok'}
app.mount('/',StaticFiles(directory='static',html=True),name='static')
