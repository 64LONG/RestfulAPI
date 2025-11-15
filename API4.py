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
#Importing ast package for data type and syntax validation
import ast

app= FastAPI()

#Blog class defintiion with variables
class Blog(BaseModel):
    blog_id: Optional[UUID] = uuid4()
    title: str = Field(default_factory="Unknown")
    content: str = Field(default_factory="Unknown")
    tags: Optional[str] = None

#In-memory Storage, an array
blogs_db = []

#API HTTP methods and definitions
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
async def read_blog(blog_id:UUID):
    for blog in blogs_db:
        if blog.blog_id == blog_id:
            return blog
    raise HTTPException(status_code=404,detail="blog not found")
#Testing API with HTTP GET via curl command
#curl -v http://127.0.0.1:8000/get-message?name=Toast

#Option #4 --- Updating blog by id
@app.put("/blogs/{blog_id}", response_model=Blog)
async def update_blogs(blog_id: UUID, updated_blog: Blog):
    for index, blog in enumerate(blogs_db):
            if blog.blog_id == blog_id:
                updated_blog.blog_id = blog_id
                blogs_db[index] = updated_blog
                return updated_blog
    raise HTTPException(status_code=404,detail="blog not found")


#Testing API with HTTP GET via curl command
#curl -v http://127.0.0.1:8000/get-message?name=Toast

#Option #5 --- Deleting blog by id
@app.delete("/blogs/{blog_id}", response_model=Blog)
async def delete_blogs(blog_id: UUID):
    for index, blog in enumerate(blogs_db):
        if blog.blog_id == blog_id:
            return blogs_db.pop(index)
    raise HTTPException(status_code=404,detail="blog not found")
#Testing API with HTTP GET via curl command
#curl -v http://127.0.0.1:8000/get-message?name=Toast


#Reference: https://blog.postman.com/how-to-build-an-api-in-python/
#Reference: https://arjancodes.com/blog/building-rest-apis-with-python-and-fastapi-tutorial/


#User Command line tool to use API HTTP methods and definitions
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
            all_blogs = requests.get('http://127.0.0.1:8000/blogs')
            print(all_blogs.text)
        #User input |  Reading a blog by ID within the array
        if var1 == "3":
            all_blogs = requests.get('http://127.0.0.1:8000/blogs')
            clean=(all_blogs.text)
            recon=ast.literal_eval(clean)
            transposed_data = list(zip(recon))
            for index,value in enumerate(transposed_data):
                print(f"Index: {index}, Value: {value}")
            x=input("Please select a number to pull up a blog: ")
            clean_x=int(x)
            print(list(transposed_data[clean_x]))
            y=list(transposed_data[clean_x])
            #grabing the list from the array and try the results as a dict
            z=y[0]
            uniq=z["blog_id"]
            test = requests.get('http://127.0.0.1:8000/blogs/'+uniq)
            print(test.text)
        if var1 == "4":
            all_blogs = requests.get('http://127.0.0.1:8000/blogs')
            clean=(all_blogs.text)
            recon=ast.literal_eval(clean)
            transposed_data = list(zip(recon))
            for index,value in enumerate(transposed_data):
                print(f"Index: {index}, Value: {value}")
            x=input("Please select a number to pull up a blog: ")
            clean_x=int(x)
            print(list(transposed_data[clean_x]))
            y=list(transposed_data[clean_x])
            #grabing the list from the array and try the results as a dict
            z=y[0]
            uniq=z["blog_id"]
            key_values=list(z.keys())
            print(key_values)
            for index,keys in enumerate(key_values):
                print(f"Index: {index}, Value: {keys}")
            x=input("Please select an index number to pull up a key data field to edit: ")
            clean_x=int(x)
            selected_key_value=key_values[clean_x]
            replacement_value=input("Please data to replace values for key pairing: ")
            org = requests.get('http://127.0.0.1:8000/blogs/'+uniq)
            print(org.text)
            prep1_org=ast.literal_eval(org.text)
            print(prep1_org)
            prep1_org.update({selected_key_value:replacement_value})
            url='http://127.0.0.1:8000/blogs/'+uniq
            print(prep1_org)
            editing_res = requests.put(url, json=prep1_org)
            print(editing_res.raw.decode_content)
            print(editing_res.status_code)
            print(editing_res.content.decode())
        if var1 == "5":
            all_blogs = requests.get('http://127.0.0.1:8000/blogs')
            clean=(all_blogs.text)
            recon=ast.literal_eval(clean)
            transposed_data = list(zip(recon))
            for index,value in enumerate(transposed_data):
                print(f"Index: {index}, Value: {value}")
            x=input("Please select a number to pull up a blog: ")
            clean_x=int(x)
            print(list(transposed_data[clean_x]))
            y=list(transposed_data[clean_x])
            #grabing the list from the array and try the results as a dict
            z=y[0]
            uniq=z["blog_id"]
            trash = requests.delete('http://127.0.0.1:8000/blogs/'+uniq)
            print(trash.text)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Failure with API processing")

try:
    API_Interface()
except:
    print("Unable to reach API interface")
