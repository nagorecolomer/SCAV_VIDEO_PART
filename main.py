#main
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hola Uri,estoy probando"}
