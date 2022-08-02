# 데이터 수집기

import asyncio
import aiohttp
from app.config import get_secret

# 네이버 오픈 API를 이용한 데이터 수집
class NaverBookScraper:
    
    NAVER_API_BOOK = "https://openapi.naver.com/v1/search/book" # 주소가 잘못됨
    NAVER_API_ID = get_secret("NAVER_API_ID")
    NAVER_API_SECRET = get_secret("NAVER_API_SECRET")   
    
    # 데이터 요청 함수
    @staticmethod
    async def fetch(session, url, headers):
        async with session.get(url, headers=headers) as response:
            if response.status == 200: # 성공
                result = await response.json()
                return result["items"]

    def unit_url(self, keyword, start):
        return {
            "url": f"{self.NAVER_API_BOOK}?query={keyword}&display=10&start={start}", # 데이터 10개(display)
            "headers": {
                "X-Naver-Client-Id": self.NAVER_API_ID,
                "X-Naver-Client-Secret": self.NAVER_API_SECRET,
            },
        }

    async def search(self, keyword, total_page):
        apis = [self.unit_url(keyword, 1 + i * 10) for i in range(total_page)]
        async with aiohttp.ClientSession() as session:
            all_data = await asyncio.gather(
                *[NaverBookScraper.fetch(session, api["url"], api["headers"]) for api in apis]
            )
            result = [] # [한 페이지에 10개의 데이터들]
            for data in all_data:
                if data is not None: # 데이터가 있는 경우에
                    for book in data:
                        result.append(book)
            return result

    def run(self, keyword, total_page):
        return asyncio.run(self.search(keyword, total_page))

# 테스트
if __name__ == "__main__":
    scraper = NaverBookScraper()
    print(scraper.run("파이썬", 3)) # (검색어, 가져올 페이지 수)
    print(len(scraper.run("파이썬", 5)))