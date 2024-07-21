from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
import requests

app = FastAPI()

PROXY_URL = "https://dashscope.aliyuncs.com"
BEARER_TOKEN = "sk-e7197f1582324f47b7f4fef9f88f533b"  # 替换为你的 Bearer Token


@app.post("/{path:path}")
async def proxy_post(path: str, request: Request):
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }

    body = await request.json()
    response = requests.post(f"{PROXY_URL}/{path}", json=body, headers=headers, verify=False)

    try:
        json_response = response.json()
    except requests.exceptions.JSONDecodeError:
        return Response(content=response.content, status_code=response.status_code,
                        media_type=response.headers.get('Content-Type'))

    return JSONResponse(content=json_response, status_code=response.status_code)


@app.get("/{path:path}")
async def proxy_get(path: str, request: Request):
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

    params = dict(request.query_params)
    response = requests.get(f"{PROXY_URL}/{path}", params=params, headers=headers, verify=False)

    try:
        json_response = response.json()
    except requests.exceptions.JSONDecodeError:
        return Response(content=response.content, status_code=response.status_code,
                        media_type=response.headers.get('Content-Type'))

    return JSONResponse(content=json_response, status_code=response.status_code)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
