from fastapi import FastAPI

app= FastAPI()

static_string = "Inital Text"

#@app.get("/get-message")
@app.get("/get-message")
async def personal(name:str):
    return {"message": "Congrats " + name +"!" " This is your API!"}
#Testing API with HTTP GET via curl command
#curl -v http://127.0.0.1:8000/get-message?name=Toast

#inital Static String
@app.post("/add")
async def add_text(text:str):
    global static_string
    static_string += text
    return {"message": "Text added", "current_string ": static_string}
#Testing API with HTTP POST via curl command
#curl -X POST -v http://127.0.0.1:8000/add?text=bye

@app.put("/change")
async def chang_text(new_text:str):
    global static_string
    static_string = new_text
    return {"message": "Text Changed", "current_string": static_string}
#Testing API with HTTP PUT via curl command
#curl -X PUT -v http://127.0.0.1:8000/change?new_text=toast

@app.delete("/remove")
async def remove_text():
    global static_string
    static_string = ""
    return {"message": "Text Removed"}
#Testing API with HTTP DELETE via curl command
#curl -X DELETE -v http://127.0.0.1:8000/remove


#http://127.0.0.1:8000/get-message?name=Toast
#The url requires the "name" parameter to be pass to allow open properly.

#Reference: https://blog.postman.com/how-to-build-an-api-in-python/
