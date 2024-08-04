from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes.users import router as users

config = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.client = MongoClient(config["URI"])
    app.database = app.client[config["DATABASE"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.client = MongoClient(config["URI"])
    app.client.close()
    
app.include_router(users, tags=["users"], prefix="/users")
