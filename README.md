# demo-task

### This is a Demo REST API built with Django Rest Framework, and uses Postgresql as a DBMS and DRF Token based Authentication, Developed and tested on a debian based linux distro.

## Set-Up Instructions:

### Configure Postgresql:

_these instructions are tested on Debian based linux distro_

1. run `sudo apt update`.
2. run `sudo apt install postgresql-14`.
3. run `service postgresql start` after that make sure the service is running by using `service postgresql status`.
4. change to postgres user by running `sudo su postgres`.
5. type `psql` to enter postgresql shell.
6. now create a new database user by typing `CREATE USER <choose_a_username> WITH PASSWORD '<choose_a_password>';` in the postgresql shell.
7. it will come in handy later for running tests that you add CREATEDB role to your new user by typing `ALTER USER <your_user_name> CREATEDB;`.
8. now create the actual DB that we will gonna use for this project by typing `CREATE DATABASE <db_name>`.


### Deploy the project:

1. create a new python virtual environment `python3 -m venv drf-task` and activate it `source drf-task/bin/activate`. 
2. Clone this repo by runnin `git clone https://github.com/0xSaltyHash/demo-task`.
3. move to the project directory `cd demo-task`.
4. install the dependencies by running `pip install -r requiremnets.txt`.
5. create empty file and name it .env `touch .env`
6. run `python -c "import secrets; print(secrets.token_urlsafe())"` to generate a secret key and copy the output.
7. open the `.env` file and add this line `SECRET_KEY = <token_you_got_from_step_6>` _note: add the token with no quotes_.
8. add `DB_USER=<your_database_user_name>` , add `DB_PASS=<your_db_password>`, add `DB_NAME=<name_of_db>`.

_Note: if you are hosting your psql DB on a server you should edit demo-task/settings.py and change HOST and PORT of the DB server_

9. now run `python manage.py makemigrations` then run `python manage.py migrate`
10. to deploy the application locally run python manage.py runserver

### Manual testin:

#### The API has 3 endpoints `api/products/` ,`api/register`, `api/login`.

* `api/register` is used to register new users accepts only `POST` requests and expects a json body, to test it run 
```
curl -X POST http://127.0.0.1:8000/api/register \
-H 'Content-Type: application/json' \
-d '{"username":"username1", "email":"testmail@mail.com", "password":"pass2311", "password2":"pass2311"}'
```

and it should return 

```
{"username":"username1","email":"testmail@mail.com"}
```

* `api/login` will generate authorization token for a registered user to be able to interact with the API, and also it accepts only `POST` requests, to test it run
```
curl -X POST http://127.0.0.1:8000/api/login \
-H 'Content-Type: application/json' \
-d '{"username":"username1", "password":"pass2311"}'
```

it should return 
```
{"token":"<random_token>"}
```

* `api/products/` is the api endpoint used to list and create products, to interact with it you should pass the authentication token in http Authorization Header, to test it:

1. list products:

```
curl -X GET  http://127.0.0.1:8000/api/products/ \
-H 'Authorization: token <your_token>'
```

will give a json response containing all products stored in our DB ordered by price.

2. filter by username:

```
 curl -X GET  http://127.0.0.1:8000/api/products/?username=<username> \
 -H 'Authorization: token <your_token>'
```

this should return a json object containing all products created by a user but if a user exists but no he didn'g create any order it will return empty list, and if the username doesn't exist it will return `Not found` error.

3. Create a new product:

```
curl -X POST  http://127.0.0.1:8000/api/products/ \
-H 'Authorization: token <your_token>' \
-H 'Content-Type: application/json' \
-d '{"product_name":"prodname", "price":100}'
```

it will return 

```
{"seller":"username1","product_name":"prodname","price":100.0}
```


### Run unit tests:

`python manage.py test api`