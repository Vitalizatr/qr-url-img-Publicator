import httpx
from fastapi import Request

class URLPublicatorAPI:
    def __init__(self, http_client: httpx.AsyncClient, api_key: str):
        self._client = http_client
        self._api_key = api_key

    async def public_qr(self,qr_code : str):
        try:
            data = {"image":  qr_code}
            params = {"key": self._api_key}

            response = await self._client.post("/1/upload", data=data, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"Ошибка внешнего API: {e.response.status_code}")
            raise e

    @classmethod
    def as_dependency(cls, request: Request) -> "URLPublicatorAPI":
        http_client = request.app.state.http_client
        return cls(http_client=http_client,api_key=request.app.state.api_key)
