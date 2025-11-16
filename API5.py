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
#Importing sqlite package for database integration
import sqlite3
#Importing asynccontextmanager package for application startup and tear down directions
from contextlib import asynccontextmanager

#app= FastAPI()

#Permenant Storage, an database
DB_Path="blogs.db"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connecting to a specfic database file, but automatic creation if none
    db= sqlite3.connect(DB_Path)
    # Return rows as dictonary objects
    db.row_factory = sqlite3.Row
    app.state.db = db
    #return db_connection
    #Create table if it doesn't exist
    db.execute("""
    CREATE TABLE IF NOT EXISTS blogs (
        blog_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        tags TEXT
    )
""")
    db.commit()

    print("Database connected and ready!")

    #Yield to app by pauses the function to alllow it to resume where it leaves off
    yield

    #Shutdown: Close Database
    db.close()
    print("Database closed!")

app= FastAPI(lifespan=lifespan)

#Blog class defintiion with variables
class Blog(BaseModel):
    #blog_id: str 
    title: str = Field(default="Unknown")
    content: str = Field(default="Unknown")
    tags: Optional[str] = None

#API HTTP methods and definitions

#Option "test" --- Connection test for Sanity Test
@app.get("/")
async def read_root():
    return {"Hello": "World"}    

#Option #1 --- Creating blog and adding into array
@app.post("/blogs")
async def create_blog(blog:Blog):
    blog_id=str(uuid4())
    
    db= app.state.db
    db.execute(
        "INSERT INTO blogs (blog_id, title, content, tags) VALUES(?,?,?,?)",
        (blog_id, blog.title,blog.content,blog.tags),

    )
    db.commit()
    return{"message":"Blog created", "blog_id": blog_id}

#Option #2 --- Read all blogs within the array
@app.get("/blogs", response_model=List[Blog])
async def read_blogs():
    db =app.state.db
    rows=db.execute("SELECT * FROM blogs").fetchall()
    return [dict(row) for row in rows]


#Option #3 --- Looking up blog and reading it by id
@app.get("/blogs/{blog_id}", response_model=Blog)
async def read_blog(blog_id:str):
    db = app.state.db
    row=db.execute("SELECT * FROM blogs WHERE blog_id = ?", (blog_id,)).fetchone()
    return dict(row)
    raise HTTPException(status_code=404,detail="blog not found")

#Testing API with HTTP GET via curl command
#curl -v http://127.0.0.1:8000/get-message?name=Toast

#Option #4 --- Updating blog by id
@app.put("/blogs/{blog_id}")
async def update_blog(blog_id: str,blog: Blog):
    db = app.state.db
    db.execute("""
        UPDATE blogs
        SET title = ?, content = ?, tags = ?
        WHERE blog_id = ?
    """, (blog.title,blog.content,blog.tags, blog_id))

    db.commit()

    if db.total_changes == 0:
        raise HTTPException(status_code=404,detail="blog not found") 
    
    return {"message": "Blog updated"}

#Testing API with HTTP GET via curl command
#curl -v http://127.0.0.1:8000/get-message?name=Toast

#Option #5 --- Deleting blog by id
@app.delete("/blogs/{blog_id}")
async def delete_blog(blog_id: str):
    db = app.state.db
    db.execute(
        "DELETE FROM blogs WHERE blog_id = ?",
        (blog_id,)
    )
    db.commit()

    if db.total_changes == 0:
        raise HTTPException(status_code=404,detail="blog not found") 
    
    return {"message": "Blog deleted"}    

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
            url='http://127.0.0.1:8000/blogs'
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
            recon=all_blogs.json()
            for index,blog in enumerate(recon):
                print(f"Index: {index}, Value: {blog}")
            x=input("Please select a number to pull up a blog: ")
            clean_x=int(x)
            y=recon[clean_x]
            #grabing the list from the array and try the results as a dict
            uniq=y["blog_id"]
            test = requests.get('http://127.0.0.1:8000/blogs/'+uniq)
            print(test.text)
        if var1 == "4":
            all_blogs = requests.get('http://127.0.0.1:8000/blogs')
            clean=(all_blogs.text)
            recon=all_blogs.json()
            for index,blog in enumerate(recon):
                print(f"Index: {index}, Value: {blog}")
            x=input("Please select a number to pull up a blog: ")
            clean_x=int(x)
            y=recon[clean_x]
            #grabing the list from the array and try the results as a dict
            uniq=y["blog_id"]
            key_values=list(y.keys())
            print(key_values)
            for index,keys in enumerate(key_values):
                print(f"Index: {index}, Value: {keys}")
            value_pointer=input("Please select an index number to pull up a key value field to edit: ")
            clean_value_pointer=int(value_pointer)
            selected_key_value=key_values[clean_value_pointer]
            replacement_value=input("Please data to replace values for key pairing: ")
            org = requests.get('http://127.0.0.1:8000/blogs/'+uniq)
            print(org.text)
            prep1_org=org.json()
            prep1_org.update({selected_key_value:replacement_value})
            url='http://127.0.0.1:8000/blogs/'+uniq
            print(prep1_org)
            editing_res = requests.put(url, json=prep1_org)
        if var1 == "5":
            all_blogs = requests.get('http://127.0.0.1:8000/blogs')
            clean=(all_blogs.text)
            recon=all_blogs.json()
            for index,blog in enumerate(recon):
                print(f"Index: {index}, Value: {blog}")
            x=input("Please select a number to pull up a blog: ")
            clean_x=int(x)
            print(recon[clean_x])
            y=recon[clean_x]
            #grabing the list from the array and try the results as a dict
            uniq=y["blog_id"]
            trash = requests.delete('http://127.0.0.1:8000/blogs/'+uniq)
            print(trash.text)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Failure with API processing")

try:
    API_Interface()
except:
    print("Unable to reach API interface")
