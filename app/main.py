from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

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