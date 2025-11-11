from fastapi import FastAPI

app= FastAPI()

#@app.get("/get-message")
@app.get("/get-message")
async def personal(name:str):
    return {"Message": "Congrats " + name +"!" " This is your API!"}

#How to test with URL with HTTP GET -> http://127.0.0.1:8000/get-message?name=Toast
#The url requires the "name" parameter to be pass to allow open properly.

#Reference: https://blog.postman.com/how-to-build-an-api-in-python/
