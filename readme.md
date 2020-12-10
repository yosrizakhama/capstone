Udacity Full-Stack Developer Nanodegree Capstone Project
This project is the final project for my Udacity FullStack Developer Nanodegree.
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

This Application does not have a frontend implemented. It is a API REST.

Application Heroku Link
https://yosritestapp.herokuapp.com/

Application Stack
The Application Tech Stack includes:

Python3: The server language
Flask: Server Framework
PostgreSQL: Database of choice
SQLAlchemy: ORM of choice to communicate between the python server and the Postgres Database. Flask SQLAlchemy is directly used.
Heroku: Deployment Platform
Application Dependencies
Library	Version
alembic	1.4.2
click	7.1.2
ecdsa	0.15
Flask	1.1.2
Flask-Cors	3.0.8
Flask-Migrate	2.5.3
Flask-Moment	0.10.0
Flask-Script	2.0.6
Flask-SQLAlchemy	2.4.4
future	0.18.2
gunicorn	20.0.4
itsdangerous	1.1.0
Jinja2	2.11.2
jose	1.0.0
Mako	1.1.3
MarkupSafe	1.1.1
psycopg2-binary	2.8.5
pyasn1	0.4.8
pycryptodome	3.3.1
python-dateutil	2.8.1
python-editor	1.0.4
python-jose	3.1.0
python-jose-cryptodome	1.3.2
rsa	4.6
six	1.15.0
SQLAlchemy	1.3.18
Werkzeug	1.0.1
Working with the application locally
Make sure you have Python installed.

Clone the Repository

git clone -b master https://github.com/yosrizakhama/capstone.git

Install Dependencies:

pip install -r requirements.txt
Export Environment Variables Refer to the setup.bash file and export the environment variables for the project.

Create Local Database: Create a local database and export the database URI as an environment variable with the key DATABASE_PATH.

Run Database Migrations:

python manage.py db init
python manage.py db migrate
python manage.py db upgrade
Run the Flask Application locally:

export FLASK_APP=app
export FLASK_ENV=development
flask run

Endpoints
The Host for the endpoints is: https://yosritestapp.herokuapp.com/

OR https://localhost:5000/ if the flask app is being run locally.

Index /
The index endpoint that indicates the Flask Application is running normally.
Response:

Type: String
Body: app running ok

Auth /auth
Returns the authorize URL that redirects to the Auth0 login page.
Response:

Type: JSON
Body:
{
    "url":"https://fsnd-yosri.eu.auth0.com/authorize?audience=CapstoneAPI&response_type=token&client_id=zVBlYiIOMSTh9BG40ycoZX5Z91AmKeA4&redirect_uri=https://yosritestapp.herokuapp.com/"
}
GET /actors
Returns a  list of actors 
It is an endpoint available to all three roles

When successful,
It returns a status code of 200, and

{
    "success": True,
    "code": 200,
    "message": "ACTORS DETAILS OK",
    "actors": list of actors_res,
    "nbr_actors": total number of actors
}
actors is an array of the actors and their details, an example:

{
    "actors": [
        "Todo : \n-ID: 2\n-name: zakhama Yosri\n-age: 41\n-genre: M",
        "Todo : \n-ID: 3\n-name: Mrabet Zohra\n-age: 66\n-genre: F",
        "Todo : \n-ID: 4\n-name: Attia Mohamed\n-age: 66\n-genre: M",
        "Todo : \n-ID: 5\n-name: Gaddab Younes\n-age: 42\n-genre: M",
        "Todo : \n-ID: 1\n-name: Leonardo De Caprio\n-age: 65\n-genre: M"
    ],
    "code": 200,
    "message": "ACTORS DETAILS OK",
    "nbr_actors": 5,
    "success": true
}
POST /actors
It takes new actor details as a JSON body
Only the manager and admin can perform this action
Actor details must have these at minimum:

{
            "name": "ADEL IMEM",
            "age": 79,
            "genre": "M"
}
Age must be an integer
There must be no empty or missing entries
It returns a status code of 200, and:

{
        "success": True,
        "code": 200,
        "message": name of actor+" ADDED OK",
        "actors": [description of all actors]
}

PATCH /actors/<int:id>
only for admin or manager
It takes the actor id to be patched, and It takes new informations of the actor details as a JSON body for example:
{
    "name": "Leonardo De Caprio",
    "age": 65,
    "genre": "M"
}
https://yosritestapp.herokuapp.com/actors/4 would delete the actor with an id of 4
Only the manager and admin can perform this action
Actor with the inputted id must exist in the database

It returns a status code of 200, and:

{
    "success": True,
    "code": 200,
    "message": "UPDATE OK",
    "id": id,
    "actor":description of the actor
}
where id is the id of the updated record
Where actor is a python dictionary of the actor details

DELETE /actors/<int:id>
only for admin
where id is the existing model id
it responds with a 404 error if id is not found
it deletes the corresponding row for id
Only admin can perform this action
returns a status code of 200 and:
{
    "success": True,
    "code": 200,
    "message": "DELETE OK",
    "id": id
}



GET /movies
Returns a  list of movies 
It is an endpoint available to all three roles
When successful,
It returns a status code of 200, and
{
    "success": True,
    "code": 200,
    "message": "MOVIES DETAILS OK",
    "movies": array of desciption informations of all movies,
    "nbr_movies": total number of movies 
}
example :
{
    "code": 200,
    "message": "MOVIES DETAILS OK",
    "movies": [
        "Todo : \n-ID: 2\n-title: Al Jazira",
        "Todo : \n-ID: 3\n-title: Ahlan zawji",
        "Todo : \n-ID: 4\n-title: El Malek",
        "Todo : \n-ID: 1\n-title: A movie updated informations"
    ],
    "nbr_movies": 4,
    "success": true
}

POST /movies
only for admin or manager
It takes new movie details as a JSON body
Movie details format:

{
    "title": "Movie Test",
    "date": "2020-12-10"
}
The title and date keys must not be null
It returns a status code of 200, and:
example :
{
    "code": 200,
    "message": "Lord of the rings ADDED OK",
    "movies": ["Todo : \n-ID: 5\n-title: Lord of the rings"],
    "success": true
}

PATCH /movies/<int:id>
only for admin or manager
It takes the movie id to be patched, for example:
https://yosritestapp.herokuapp.com/actors/4

Movie with the inputted id must exist in the database
It takes the movie details to be updated as a JSON body
Movie details can have all or none of these:

{
    "title": "another day",
    "date": "2020-12-12"
}
No key should have a null value
Instead omit it completely
If successful:
It returns a status code of 200, and:

{
    "code": 200,
    "id": 1,
    "message": "UPDATE OK",
    "movie": "Todo : \n-ID: 1\n-title: another day",
    "success": true
}


DELETE /movies/<int:id>
only for admin 
where id is the existing model id it responds with a 404 error if id is not found it deletes the corresponding row for id returns status code 200 and:

{
    "success": True,
    "code": 200,
    "message": "DELETE OK",
    "id": id
}
where id is the id of the deleted record

##
GET /movies/<int:id>
Returns a  list of actors foreach movie 
It is an endpoint available to all three roles
id is integer refer to the id of the movie
When successful,
It returns a status code of 200, and
{
        "success": True,
        "code": 200,
        "message": "MOVIES DETAILS OK",
        "movies": [actors informations for movie],
        "nbr_movies": len(movies_res)
}
example :
{
    "code": 200,
    "message": "MOVIES DETAILS OK",
    "movies": [
        "Todo : \n-ID: 3\n-name: Mrabet Zohra\n-age: 66\n-genre: F",
        "Todo : \n-ID: 4\n-name: Attia Mohamed\n-age: 66\n-genre: M"
    ],
    "nbr_movies": 2,
    "success": true
}

POST /movies/<int:id>
only for admin or manager
It takes the id actor to add as an actor in the movie details as a JSON body
details format:

{
    "id":"7"
}
It returns a status code of 200, and:
{
    "success": True,
    "code": 200,
    "message": " ADDED OK",
    "movies": id
}
example :
{
    "code": 200,
    "message": " ADDED OK",
    "movies": 1,
    "success": true
}


DELETE /movie_actors/<int:id>
only for admin 
where id is the existing movie id it responds with a 404 error if id is not found it deletes the corresponding row for id returns status code 200 and:

{
    "code": 200,
    "message": " DELETED OK",
    "movies": 1,
    "success": true
}
where id is the id of the deleted record


## Testing
To run the tests, run
```
1 - Dropdb capstone
2 - Createdb capstonetest and psql capston < capstone.psql
    or
        open psql and after that:
        Dropdb capstonetest,write this request CREATEdb capstone WITH TEMPLATE=capstone;
3 - python test_flaskr.py
```
##
Roles and Permissions

I/ Permssions :
- get:movies	gettinig informations from movies	
- get:actors	gettinig informations from actors	
- put:movies	add movies	
- put:actors	add actors	
- delete:actors	delete actors	
- delete:movies	delete movies	
- update:actors	update information of actors	
- update:movies	update information of movies	
- get:movie_actors	get list of actors from movie	
- add:actors_movie	add actors from movie	
- del:actors_movie	delete actors from movie

II/ The application has 3 roles setup:

1) admin
description : all access for database - all permission are allowed
Can get all actors in the database
Can get all movies in the database
Can add actors in the database
Can add movies in the database
Can update all actors in the database
Can update movies in the database
Can delete actors in the database
Can delete movies in the database

2) manager

description : can get and update information but can't delete
Can get all actors in the database
Can get all movies in the database
Can add actors in the database
Can add movies in the database
Can update all actors in the database
Can update movies in the database

3) user
	description : simple user can only show informations
All permissions of the casting director
Can get all actors in the database
Can get all movies in the database