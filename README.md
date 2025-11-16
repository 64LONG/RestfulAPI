# RestfulAPI
API project utilizing python

======================================
API Development
======================================
An admin's first journey into backend development using python. 

Utilizing project from roadmap.sh for requirements and direction:

https://roadmap.sh/projects/blogging-platform-api


-------------------------------------------
Prerequisuites
-------------------------------------------
1. Install python in your distro via source code or obtain a linux distro with python
ADMIN NOTE: I started with Debian, and come to Fedora for stablility and ready out of the box.

2. Install IDE of your choice.

EXAMPLE: microsoft Visual Code Studio
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\nautorefresh=1\ntype=rpm-md\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/vscode.repo > /dev/null

dnf check-update

sudo dnf install code

3. Install Git for CI/CD

sudo dnf install git-all

4. Install the nessecary libary or packages using python
#FastAPI is python libray for web framework to allow development of an API 
"FastAPI" libary | pip install fastapi

#uvicorn is python libray for ASGI web server implementatiion
"uvicorn" libary | pip install uvicorn

#Pydantic is python libray for data classification and data type development 
"pydantic" libary | pip install pydantic

#typing is python libray for hinting data types while doing development
"typing" libary | pip install typing

#uuid is python libray for unique identifiers
"uuid" libary | pip install uuid

#requests is python libray for HTTP methods and requests to websites 
"requests" libary | pip install requests


5. Install curl for API testing

sudo apt install curl

or

sudp dnf install curl


-------------------------------------------
Operations Flow
-------------------------------------------
Utilize the FastAPI modules for packages to build out our application
i.e., from fastapi import FastAPI

Utilize the uvicorn from the command line to initalize and test the API written your python script.
i.e, uvicorn API:app --reload
NOTE1: The "API" portion is the name of the file.
NOTE2: The "app" portion is the name of the variable that calls out the defined API function.
NOTE3: The "--reload" option allows the API to be immedaitely updates with any change to the file. 

Run the API script
