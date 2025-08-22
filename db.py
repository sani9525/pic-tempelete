import asyncpg
import os
from dotenv import load_dotenv
import ssl

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def get_connection():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False  # 🚨 disable hostname verification
    ssl_context.verify_mode = ssl.CERT_NONE  # 🚨 ignore self-signed cert
    return await asyncpg.connect(
        DATABASE_URL,
        ssl=ssl_context
    )

