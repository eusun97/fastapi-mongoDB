from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models import mongodb

base_dir = Path(__file__).resolve().parent

app = FastAPI()

# app.mount("/static",StaticFiles(directory=Path(__file__).parent.absolute() / "static"),name="static")

templates = Jinja2Templates(directory=base_dir / "templates")


@app.get("/", response_class=HTMLResponse) 
async def root(request: Request):
    return templates.TemplateResponse(
        "./index.html", 
        {"request": request, "title" : "콜렉터 북북이"},
        )

# 검색 router
@app.get("/search", response_class=HTMLResponse) 
async def search(request: Request, q: str): # 검색어 쿼리 받기
    return templates.TemplateResponse(
        "./index.html", 
        {"request": request, "title" : "콜렉터 북북이", "keyword" : q},
        )
    
# 이벤트 등록 (데이터베이스 처음에 연결하고 서버가 다운되면 끊기도록)    
@app.on_event("startup")
def on_app_start(): # 앱이 처음 시작될 때 on_app_start 함수 시작
    """before app starts"""
    mongodb.connect()
    

@app.on_event("shutdown")
def on_app_shutdown(): # 서버가 shutdown이 됐을 때 실행되는 함수
    """after app shutdown"""
    # mongodb.close()