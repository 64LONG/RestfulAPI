from fastapi import FastAPI

app= FastAPI()

#@app.get("/get-message")
@app.get("/get-message")
async def read_root():
    return {"Message": "Congrats! This is your first API!"}

#Reference: https://blog.postman.com/how-to-build-an-api-in-python/
