import uvicorn
import logging
import os
import uuid
import time
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from datetime import datetime, timezone
from agents import set_default_openai_key

from app.api.v1.responses.api_error import APIError
from app.api.v1.responses.info import ResponseInfo
from app.utils.commons import get_attributes_from_pyproject
from app.utils.logger import setup_logging
from app.api.auth.verify import verify_jwt_token
from app.api.v1.responses.exception_handlers import register_exception_handlers

from app.api.v1.router import router as router_v1 

##############################
#                            #
#                            #
#         API CONFIG        #
#                            #
#                            #
##############################

# Global variables
load_dotenv(find_dotenv(".env"))
set_default_openai_key(os.getenv("KEY_OPENAI"))
DEPLOYED_SERVICE = True if os.getenv('ENV_DEPLOYED_SERVICE')=='1' else False
setup_logging(
    None,
    level=logging.INFO if DEPLOYED_SERVICE else logging.INFO
)
if DEPLOYED_SERVICE:
    logging.info("Running in deployed mode")
else:
    logging.info("Running in local mode")
CONFIG = get_attributes_from_pyproject()

# App init
app = FastAPI(
    title=CONFIG.get('name'),
    version=CONFIG.get('version'),
    description=CONFIG.get('description'),
    docs_url='/docs' if not DEPLOYED_SERVICE else None, #type: ignore
    redoc_url='/redoc' if not DEPLOYED_SERVICE else None #type: ignore
)

# Register exception handlers
register_exception_handlers(app)

# Middleware
allowed_origins = [
    "https://butterflai.art",
    "https://butterflai.pro",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://butterflai-.*-butterfl-ai\.vercel\.app",
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PATCH'],
    allow_headers=["Content-Type", "Authorization"],
)


##############################
#                            #
#                            #
#         MIDDLEWARES        #
#                            #
#                            #
##############################

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self';"
    if response.status_code == 405:
        logging.error(f"405 Method Not Allowed - Path: {request.url.path}")
    return response


@app.middleware("http")
async def add_request_uuid(request: Request, call_next):
    request.state.request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{process_time:.4f} ms"
    return response


##############################
#                            #
#                            #
#           HEALTH           #
#                            #
#                            #
##############################
async def is_service_operational() -> bool:
    return True

@app.get(
    "/health",
    summary='Checks the system health',
    tags=["Health"],
    responses={
        200: {"description": "Operative service"},
        503: {"description": "Unavailable service"}
    }
)
async def health_check() -> JSONResponse:
    """
    Health check endpoint to verify service availability.
    Returns a status indicating whether the service is operational along with an appropriate HTTP status code.
    """
    try:
        is_service_up = await is_service_operational()
        if is_service_up:
            return JSONResponse(content={"status": "up"}, status_code=200)
        return JSONResponse(content={"status": "down"}, status_code=503)
    except Exception:
        logging.error('Error in health check!')
        return JSONResponse(content={"status": "down"}, status_code=503)
    

##############################
#                            #
#                            #
#            ROOT            #
#                            #
#                            #
##############################
@app.get(
    "/",
    tags=["Index"],
    summary="Redirects to info endpoint",
)
async def root():
    return RedirectResponse(url="info/")


##############################
#                            #
#                            #
#            INFO            #
#                            #
#                            #
##############################
@app.get(
    "/info",
    response_model=ResponseInfo,
    tags=["Info"],
    summary="Service technical details",
    responses={
        400: {"model": APIError},
        500: {"model": APIError},
    },
)
async def info(
    user_token: UserToken = Depends(verify_jwt_token),
    # request_model: RequestModel = Depends(get_request_model)
) -> ResponseInfo:
    """
    Get Service technical details
    """
    return ResponseInfo(
        utc_datetime=datetime.now(timezone.utc).isoformat(),
        name=CONFIG.get('name'),
        version=CONFIG.get('version'),
        description=CONFIG.get('description')
    )

##############################
#                            #
#                            #
#        SECURE-DATA         #
#                            #
#                            #
##############################
@app.get("/secure-data", tags=["Secure Data"])
async def secure_data(decoded_token: dict = Depends(verify_jwt_token)):
    # Your secure endpoint logic here
    return {
        "message": "Access to secure data granted",
        "user": decoded_token
    }

##############################
#                            #
#                            #
#        APP-ROUTERS         #
#                            #
#                            #
##############################
app.include_router(router_v1)
# app.include_router(router_v1, prefix="/api/v2")