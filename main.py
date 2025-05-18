import time
import fastapi.middleware
import fastapi.middleware.cors
import psycopg2
from psycopg2.extras import RealDictCursor # To get the data in dictionary format
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import post, user, auth, like
import models
from database import engine, get_db

# models.Base.metadata.create_all(bind=engine) # No longer needed after we start using alembic
app = FastAPI()


# while True:
#     # Code will not proceed further if there is any error
#     try:
#         connection = psycopg2.connect(host='localhost', database='fastapi', user='postgres',password='iEnable@123', cursor_factory=RealDictCursor)
#         #RealDictCursor returns the columns as a Dict with key as column name. Default behaviour is just to return the column values without the names of the col
#         cursor = connection.cursor()
#         print(f"*******Successfully connected to the database*******")
#         break
#     except Exception as e:
#         time.sleep(5)
#         print(f"Could not connect. Error: {e}")

origins = ["https://www.google.com"]

app.add_middleware( # Allows requests from domains on other servers. Important if you want a public API. Default is no-CORS policy
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Hello world from docker"}

app.include_router(post.router) #Include the router object from post.py, so it goes through all the path operations defined for it sequentially when we get a request
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)