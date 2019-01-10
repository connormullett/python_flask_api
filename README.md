# FLASK API's


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

