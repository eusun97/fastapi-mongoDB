'''
from typing import Optional
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get("/hello")
def read_hellofastapi():
    print("안뇽")
    return {"fastapi" : "hello"}

@app.get("/items/{item_id}/{xyz}") # 동적라우팅
def read_item(item_id : int, xyz : str, q : Optional[str] = None):
    return {"item_id" : item_id, "xyz" : xyz, "q" : q}
'''
'''
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

# 절대 경로 설정
base_dir = Path(__file__).resolve().parent # Path(__file__).resolve() : 현재 경로 / .parent : 현재 경로 main.py의 부모 폴더 app을 가리킴

app = FastAPI()

app.mount("/static",StaticFiles(directory=Path(__file__).parent.absolute() / "static"),name="static")

templates = Jinja2Templates(directory=base_dir / "templates")


@app.get("/items/{id}", response_class=HTMLResponse) # reponse 타입을 html reponse로 받는 것 
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("index.html", {"request": request, "id": id, "test" : "에헴"})
# templatees안에 TemplateResponse 클래스를 사용해서 return 받는 것
# 첫 번째 인자에는 templates안에 있는 index.html을 불러옴
# 두 번째 인자(콘텍스트)에는 index.html에 데이터를 보내는 것 {{ id }}
# 콘텍스트는 반드시 request키를 포함해야함 --> 요청에 대한 정보들이 request에 담겨있음
'''  