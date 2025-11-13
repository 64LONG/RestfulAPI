#Importing package Web API, FastAPI
from fastapi import FastAPI, HTTPException
#Importing pydantic package to classify and manage data
from pydantic import BaseModel, Field
#Importing Typing package to note expected data for variables and functions
from typing import List, Optional
#Importing UUID package for unique identifers to use
from uuid import uuid4, UUID
#Importing UUID package for unique identifers to use
import requests

app= FastAPI()

#Blog class defintiion with variables
class Blog(BaseModel):
    blog_id: Optional[UUID] = uuid4()
    title: str = Field(default_factory="Unknown")
    content: str = Field(default_factory="Unknown")
    tags: Optional[str] = None

#
# class BlogCreate(Blog):
    #pass

#class BlogwithID(Blog):
    #id: int

#In-memory Storage, an array
#blogs_db = List[Blog]
blogs_db = []


#Option "test" --- Connection test for Sanity Test
@app.get("/")
async def read_root():
    return {"Hello": "World"}    

#Option #1 --- Creating blog and adding into array
#@app.post("/blogs", response_model=Blog)
@app.post("/newblog")
async def create_blog(blog:Blog):
    blogs_db.append(blog)
    return{
        'message':' Blog Created',
        'blog' : blog
    } 

#Option #2 --- Read all blogs within the array
@app.get("/blogs", response_model=List[Blog])
async def read_blogs():
    return blogs_db

#Option #3 --- Looking up blog and reading it by id
@app.get("/blogs/{blog_id}", response_model=Blog)
async def read_blogs(blog_id:UUID):
    for blog in blogs_db:
        if blogs_db == blog_id:
            return blog
    raise HTTPException(Status_code=404,detail="blog not found")
#Testing API with HTTP GET via curl command
#curl -v http://127.0.0.1:8000/get-message?name=Dee

#Option #4 --- Updating blog by id
@app.put("/blogs/{blog_id}", response_model=Blog)
async def update_blogs(blog_id: UUID, blog: Blog):
    for index, stored_blog in enumerate(blogs_db):
        if stored_blog.id == blog_id:
            blog_db[index] = blog
            return blog
    raise HTTPException(Status_code=404,detail="blog not found")
#Testing API with HTTP GET via curl command
#curl -v http://127.0.0.1:8000/get-message?name=Dee

#Option #5 --- Deleting blog by id
@app.delete("/blogs/{blog_id}", response_model=Blog)
async def delete_blogs(blog_id: UUID):
    for index, blog in enumerate(blogs_db):
        if blog.id == blog_id:
            return blogs_db.pop(index)
    raise HTTPException(Status_code=404,detail="blog not found")
#Testing API with HTTP GET via curl command
#curl -v http://127.0.0.1:8000/get-message?name=Dee


#Reference: https://blog.postman.com/how-to-build-an-api-in-python/
#Reference: https://arjancodes.com/blog/building-rest-apis-with-python-and-fastapi-tutorial/

def API_Interface():
    """API interface for user to interact from executing script"""
    try:
        print("Welcome to the API interface for blogs")
        print("...")
        print("...")
        print("...")
        print("Welcome to the main menu! Please select your method of choice")
        print("[test] ---  Test Connecting to interface!")
        print("[1] --- Creating blog and adding into array")
        print("[2] --- Read all blogs within the array")
        print("[3] --- Looking up blog and reading it by id")
        print("[4] --- Updating blog by id")
        print("[5] --- Deleting blog by id")
        var1=input('Please enter your choice here!')
        #User input | Allowing sanity test
        if var1 == "test":
            test = requests.get('http://127.0.0.1:8000/')
            print(test.text)
        #User input | Creating blog and adding into array
        if var1 == "1":
            print("Welcome to Blog Creatation! Please provide us information for your blog.")
            input_title=input('Please enter blog title here!        ')
            clean_input_title=str(input_title)
            input_content=input('Please enter blog content here!      ')
            clean_input_content=str(input_content)
            input_tags=input('Please enter blog tags here!        ')
            clean_input_tags=str(input_tags)
            url='http://127.0.0.1:8000/newblog'
            blog_unique_id=uuid4()
            clean_blog_unique_id=str(blog_unique_id)
            myobj = {
                'blog_id':clean_blog_unique_id,
                'title':clean_input_title,
                'content':clean_input_content,
                'tags':clean_input_tags
            }
            Entry = requests.post(url, json = myobj)
            #Entry = blog(id=uuid.uuid4(), title=clean_input_title, content=clean_input_content, tags=clean_input_tags)
            print(Entry.text)
        #User input | Reading all blogs within the array
        if var1 == "2":
            print("Reading all blogs currently within the array")
            blog_stack = requests.get('http://127.0.0.1:8000/blogs')
            print(blog_stack.text)
        #User input |  Reading a blog by ID within the array
        if var1 == "3":
            print("WORK IN PROGRESS | [3] --- Looking up blog and reading it by id")
            #NOTE => Grab blog id from JSON item within blog_db array
        #User input |  Updating a blog by ID within the array
        if var1 == "4":
            print("WORK IN PROGRESS | [4] --- Updating blog by id")
        #User input |  Deleting a blog by ID within the array
        if var1 == "5":
            print("WORK IN PROGRESS | [5] --- Deleting blog by id")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Failure with API processing")

try:
    API_Interface()
except:
    print("Unable to reach API interface")
