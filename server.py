# uvicorn main:app --reload를 사용하지 않고 터미널창에 python server.py(파일명)을 입력하면 실행됨
import uvicorn

if __name__ == "__main__":
    uvicorn.run('app.main:app', host='localhost', port=8000)

