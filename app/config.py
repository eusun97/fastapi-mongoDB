import json
from pathlib import Path
from typing import Optional


BASE_DIR = Path(__file__).resolve().parent.parent # app폴더 밖에 secrets.json 배치

# secrets.json에 key와 value를 적어주면 해당하는 key를 사용해서 변수를 그대로 가져오는 함수
# 민감한 정보(secrets.json)를 파싱해서 value로 사용할 수 있게 하는 함수
def get_secret(
    key: str,
    default_value: Optional[str] = None,
    json_path: str = str(BASE_DIR / "secrets.json"),
):

    with open(json_path) as f:
        secrets = json.loads(f.read())
    try:
        return secrets[key]
    except KeyError:
        if default_value:
            return default_value
        raise EnvironmentError(f"Set the {key} environment variable.")

# 프로젝트에서 사용할 변수들 
MONGO_DB_NAME = get_secret("fastapi-pj")
MONGO_URL = get_secret("mongodb+srv://usun:1111@testcluster.o2yod.mongodb.net/fastapi-pj")
NAVER_API_ID = get_secret("B51cwkR69GpgBmNaWflD")
NAVER_API_SECRET = get_secret("JWpLOTMjdI")