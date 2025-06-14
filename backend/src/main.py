# main.py
from fastapi import FastAPI


app = FastAPI()

# Include routers


@app.get("/")
def read_root():
    return {"Hello": "World"}  # main.py
