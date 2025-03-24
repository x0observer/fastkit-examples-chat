import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.middleware.engine import init_db

from src.app.auth.register import auth_router
from src.app.chats.register import chat_router, message_router

app = FastAPI(
    debug=True,
    docs_url=os.getenv('DOCS_URL', '/docs'),
    redoc_url=os.getenv('REDOC_URL', '/redoc')
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(message_router)

@app.on_event("startup")
async def startup_event():
    """
    Perform startup actions, like initializing the database.
    """
    await init_db()
