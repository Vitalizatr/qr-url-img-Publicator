from fastapi import FastAPI,Depends, HTTPException
from services.qr_coder import QrCoder
from contextlib import asynccontextmanager
import httpx
from services.img_to_url import URLPublicatorAPI
from typing import Annotated
import os
from dotenv import  load_dotenv

load_dotenv() 

@asynccontextmanager
async def lifespan(app:FastAPI):
    api_key = os.getenv("IMGBB_API_KEY")

    app.state.api_key = api_key
    async with httpx.AsyncClient(base_url="https://api.imgbb.com", timeout=5.0) as client:
        app.state.http_client = client
        yield

qr = QrCoder()
app = FastAPI(
    title="Qr code Api",
    description="Фотография -> qr-code",
    version="0.1",
    lifespan=lifespan,
)

APIConection = Annotated[URLPublicatorAPI,Depends(URLPublicatorAPI.as_dependency)]

@app.post("/url/")
async def url_to_qr(url: str,api_service : APIConection):
    try:
        generated_qr_bytes = qr.url_to_qr(url)
        result = await api_service.public_qr(generated_qr_bytes)
        return result
        
    except httpx.HTTPStatusError as e:
        print(f"[ERROR] ImgBB API Error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code, 
            detail=f"Ошибка при публикации на ImgBB: {e.response.text}"
        )
    except Exception as e:
        print("[ERROR] Внутренняя ошибка сервера:")
        
        raise HTTPException(
            status_code=500, 
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )


@app.post("/img/")
async def url_to_qr(img: str,api_service : APIConection):
    try:
        
        result = await api_service.public_qr(img)
        generated_qr_bytes = qr.url_to_qr(result['data']['url'])
        return {
            'qr' : generated_qr_bytes
        }
        
    except httpx.HTTPStatusError as e:
        print(f"[ERROR] ImgBB API Error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code, 
            detail=f"Ошибка при публикации на ImgBB: {e.response.text}"
        )
    except Exception as e:
        print("[ERROR] Внутренняя ошибка сервера:")
        
        raise HTTPException(
            status_code=500, 
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )

