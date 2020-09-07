# Full Stack Nano Degree Capstone Project : Casting Agency


## Getting Started
### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
createdb castingAgency 

```

## Running the server

run in terminal the run.sh file which contains all commands needed to run the server

To run the server, execute:

```bash
bash run.sh
```

# API Reference

## Getting started	

the app run locally and on live server

* live server Url: https://fsnd-capstone-ahmed751995.herokuapp.com/

* local Url: http://127.0.0.1:5000/

## roles
the app has three roles:

* Casting Assistant
 - Can view actors and movies

* Casting Director
 - All permissions a Casting Assistant has and…
 - Add or delete an actor from the database
 - Modify actors or movies

* Executive Producer
 - All permissions a Casting Director has
 - Add or delete a movie from the database

each request should contains a valid jwt Token by which the role and permissions are determined.


## Error handling

Errors are returned as JSON object in the following formats:

```JSON
{
	"success": False, 
	"error": 404,
	"message": "resource not found"
}

```

the API will return an error when requests fail:

* 400: bad request
* 422: unprocessable
* 500: internal server error
* 404: resource not found
* 401: Unauthorized 

## Endpoints
[GET/movies]()

* General
  * return an object of all movies in the database with success value
* sample: curl  BaseUrl/movies

* the GET request should contains a valid jwt token
	
```json
{
    "movies": [
        {
            "id": 1,
            "release_date": "Tue, 02 Mar 2021 00:00:00 GMT",
            "title": "capstone"
        },
        {
            "id": 3,
            "release_date": "Tue, 02 Mar 2021 00:00:00 GMT",
            "title": "rush hour"
        }
    ],
    "success": true
}

```


[GET/actors]()

* General
  * return an object of all actors in the database with success value
* sample: curl  BaseUrl/actors

* the GET request should contains a valid jwt token
	
```json
{
    "actors": [
        {
            "age": 40,
            "gender": "male",
            "id": 2,
            "name": "Ahmed"
        },
        {
            "age": 18,
            "gender": "male",
            "id": 4,
            "name": "saif"
        }
    ],
    "success": true
}

```

[GET/actors]()

* General
  * return an object of all actors in the database with success value
* sample: curl  BaseUrl/actors

* the GET request should contains a valid jwt token
	
```json
{
    "actors": [
        {
            "age": 40,
            "gender": "male",
            "id": 2,
            "name": "Ahmed"
        },
        {
            "age": 18,
            "gender": "male",
            "id": 4,
            "name": "saif"
        }
    ],
    "success": true
}
```

[DELETE/movie]()

* General
  * delete a movie based on the {movie id} specified on url
  * Executive Producer is the only one who has the authorization to delete a movie

* sample: curl --location --request DELETE BaseUrl/movies/2 --header 'Authorization: Bearer $TOKEN'

* the DELETE request should contains a valid jwt token
	
```json
{
    "id": 2,
    "success": true
}
```

[DELETE/actor]()

* General
  * delete an actor based on the {actor id} specified on url
  * Executive Producer and Casting Director are the only roles who have the authorization to delete an acotr

* sample: curl --location --request DELETE BaseUrl/actors/2 --header 'Authorization: Bearer $TOKEN'

* the DELETE request should contains a valid jwt token
	
```json
{
    "id": 2,
    "success": true
}
```


[POST/actor]()

* General
  * add new actor to the database
  * Executive Producer and Casting Director are the only roles who have the authorization to post an acotr

* sample: curl --location --request POST 'BaseUrl/actors' --header 'Authorization: Bearer $TOKEN' --header 'Content-Type: application/json' --data-raw '{"name": "saif", "age": 18, "gender": "male"}'

* the POST request should contains a valid jwt token
	
```json
{
    "id": 5,
    "success": true
}
```


[POST/movie]()

* General
  * add new movie to the database
  * Executive Producer is the only roles who hase the authorization to post a movie

* sample: curl --location --request POST 'BaseUrl/movies' --header 'Authorization: Bearer $TOKEN' --header 'Content-Type: application/json' --data-raw '{"title": "jumanji", "release_date":"3-2-2021"}

* the POST request should contains a valid jwt token
	
```json
{
    "id": 5,
    "success": true
}
```


[PATCH/movie]()

* General
  * add new movie to the database
  * Executive Producer and Casting Director are the only roles who have the authorization to patch a movie

* sample: curl --location --request POST 'BaseUrl/movies/3' --header 'Authorization: Bearer $TOKEN' --header 'Content-Type: application/json' --data-raw '{"title": "rush hour 2"}'

* the PATCH request should contains a valid jwt token
	
```json
{
    "success": true
}
```

[PATCH/actor]()

* General
  * add new movie to the database
  * Executive Producer and Casting Director are the only roles who have the authorization to patch a movie

* sample: curl --location --request POST 'BaseUrl/actors/2' --header 'Authorization: Bearer $TOKEN' --header 'Content-Type: application/json' --data-raw '{"age": 40}'

* the PATCH request should contains a valid jwt token
	
```json
{
    "success": true
}
```



# Test Reference
this app contains postman and unittest,choose the one that is more convenient to you.

## postman

* import ``` castingAgency.postman_collection.json ``` into postman app 

* add the TOKEN to each role 

* run the server by typing in terminal ``` bash run.sh``` or you can you the live server by replacing the {{host}} variable value with the live server Url

* (hint) make sure that you use a proper id in delete and patch request


## unittest

* update the ```director``` , ```producer``` and ```assistant``` variables in ```test_api_setup.sh``` with a valid TOKEN 

* run in terminal ``` bash test_api_setup.sh```