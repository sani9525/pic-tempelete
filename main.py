from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.model import create_table
from pydantic import BaseModel
from routes import auth
app=FastAPI(title="Photo Template E-commerce API")

# Include routers
app.include_router(auth.router)
# app.include_router(sellers.router)
# app.include_router(templates.router)
# app.include_router(orders.router)
# app.include_router(payments.router)
# app.include_router(delivery.router)

@app.on_event("startup")
async def on_startup():
    await create_table()

@app.get("/")
async def root():
    return {"message": "Hello World"}