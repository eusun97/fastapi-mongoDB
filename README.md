# fastapi-mongoDB
# 책 정보 출처 : 비제이퍼블릭
# 책 정보 수집
# db에 출판사 / 가격 / 이미지를 포함한 데이터 100개 데이터 수집
# --> 동일한 키워드로 검색했을 때 다시 수집을 하게 되면 중복이 돼서


# db연결
1. 시크릿 변수 설정 : mongodb주소. 네이버api 시크릿 키 등
2. odmantic 라이브러리 사용 fastapi와 연걸
3. models 디렉토리를 사용하여 추상화 (odmantic코드 추상화)
4. book 모델 개발
5. db에 insert
