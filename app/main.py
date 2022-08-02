from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models import mongodb
from app.models.book import BookModel
from app.book_scraper import NaverBookScraper

base_dir = Path(__file__).resolve().parent

app = FastAPI()

# app.mount("/static",StaticFiles(directory=Path(__file__).parent.absolute() / "static"),name="static")

templates = Jinja2Templates(directory=base_dir / "templates")


@app.get("/", response_class=HTMLResponse) 
async def root(request: Request):
    # book = BookModel(keyword="파이썬", publisher="BJpublic", price=12000, image="me.png") # 예시로 데이터 넣기
    # print(await mongodb.engine.save(book)) # db에 저장 / await 붙인 이유 : save 함수가 어씽크(코루틴)함수이기에 비동기적으로 작동하기 때문
    return templates.TemplateResponse(
        "./index.html", 
        {"request": request, "title" : "콜렉터 북북이"},
        )

# 검색 router
@app.get("/search", response_class=HTMLResponse) 
async def search(request: Request, q: str): # 검색어 쿼리 받기
    # 1. 쿼리에서 검색어 추출
    keyword = q
    
    # 예외처리
    # 1) 검색어가 없다면 사용자에게 검색 요구 return
    # 2) 해당 검색어에 대해 수집된 데이터가 이미 DB에 존재한다면 해당 데이터를 보여줌 return
    if not keyword:
        return templates.TemplateResponse("./index.html", {"request": request})
    
    if await mongodb.engine.find_one(BookModel, BookModel.keyword==keyword): # 모델의 키워드가 쿼리로 받은 키워드랑 같은거 찾기
        books = await mongodb.engine.find(BookModel, BookModel.keyword == keyword)
        return templates.TemplateResponse(
        "./index.html",
        {"request": request, "title": "콜렉터 북북이", "books" : books},
    )
    
    # 2. 데이터 수집기로 해당 검색어에 대해 데이터 수집
    naver_book_scraper = NaverBookScraper()
    books = await naver_book_scraper.search(keyword, 10)
    book_models = []
    for book in books:
        book_model = BookModel(
            keyword=keyword,
            publisher=book["publisher"],
            price=book["price"],
            image=book["image"],
        )
        book_models.append(book_model)
        
    # 3. DB에 수집된 데이터를 저장한다.
    await mongodb.engine.save_all(book_models)
    #  - 수집된 각각의 데이터에 대해서 DB에 들어갈 모델 인스턴스를 찍는다.
    #  - 각 모델 인스턴스를 DB에 저장한다.
    return templates.TemplateResponse(
        "./index.html",
        {"request": request, "title": "콜렉터 북북이", "books" : books},
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