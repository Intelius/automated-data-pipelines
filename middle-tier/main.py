from fastapi import FastAPI, Depends
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

# reading the environment variables
load_dotenv()
import uvicorn

from src.processedData.endpoints import (
  newsDescription,
  oneMinute
)

app = FastAPI()

# Set up CORS to allow the frontend to communicate with the backend.
# Refer to: https://fastapi.tiangolo.com/tutorial/cors/
origins = [
  "http://localhost",
  "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(newsDescription.router)
app.include_router(oneMinute.router)


# Starting the server on port 3010
if __name__ == "__main__":
    uvicorn.run(
      app,
      host="0.0.0.0",
      port=3030
    )