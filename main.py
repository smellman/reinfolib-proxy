from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

APP_NAME = 'reinfolib-proxy'
API_KEY = 'your-api-key-here'

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info(f"{APP_NAME} is starting up...")
        yield
    finally:
        logger.info(f"{APP_NAME} is shutting down...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.middleware("http")
async def add_logging(request: Request, call_next):
    logger.info(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status code: {response.status_code}")
    return response

@app.get("/proxy/{path:path}")
async def proxy(path: str, request:Request,  response: Response):
    headers = {
        'Ocp-Apim-Subscription-Key': API_KEY
    }
    async with httpx.AsyncClient() as client:
        proxy = await client.get(f"https://www.reinfolib.mlit.go.jp/{path}", params=request.query_params, headers=headers)
    response.body = proxy.content
    response.status_code = proxy.status_code
    return response