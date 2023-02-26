# Overview

A simple backend of a FastAPI CRUD application, providing user authentication functionality (SignUp, SignIn and SignOut) and handling resources stored in a PosgreSQL database.

## Local Deployment

Clone the repository

```bash
git clone https://github.com/SoFish1/crud_app.git

cd crud_app

docker-compose up -d
```

## CRUD operations

This app provides a simple user interface for performing CRUD operations on a list of resources. Users can:

* Create a new resource
* Read an existing resource
* Read all existing resources
* Read all existing resources which have been created in a specific time interval
* Update an existing resource
* Delete an existing resource

The API is implemented using the FastAPI framework in Python, and the data is stored in a PosgreSQL database.


## Testing

A testing module is also provided to test the endpoint.
To perform the tests run the following command in the project folder (or directly in the docker container):

```bash
    pytest -v   
```
A PGAdmin service is also provided to visualize the database and to check that everyting is as expected.

