# Basic Flask API

This API supports CRUD functionality on two different models and implements 
foreign keys to demonstrate how to build a functional API in flask

`full_api.py` is the full api
The other `xxx_api.py` files are sections for specific HTTP verbs

## Prerequisites
- Python3
- Postman or other API testing tool
-Postgres
- This repo

## Installing Packages
- clone the repository
- open file location in terminal
- `pip install -r requirements.txt`

## Initial Config
- log in to Postgres or open PGAdmin
- Create database called `flask_api`
- Change `postgres:password` on line 8 in `full_api.py` to match your postgres username and password
- Open Python3 interpreter from the repos base directory in terminal 
- run the two commands below to initiate the 2 models in `full_api.py`
    ```Python3
   from full_api import db
   db.create_all()
    ```
- Exit interpreter and run `full_api.py` with the command below
    `python3 full_api.py`
- open Postman (or other tool) and send requests to `http://localhost:8080`

## Sample Requests
plug the following requests into postman to test the API

url:`localhost:8080/user/signup` method: `POST`
creates a simple user
```json
{
"username": "test_user",
"email": "test@test.com"
}
```

url: `localhost:8080/` method: POST
```json
{
"name": "Python",
"framework": "Django",
"owner_id": 1
}
```

Note that in the 2cnd POST request we manually give the owner id, a front end app would take care
of getting this value well before the post is made

Use a GET request on the following URL to see our Data

`localhost:8080/1` to view the first entry

or 

`localhost:8080` to view ALL of our entries (if you choose to add more)

