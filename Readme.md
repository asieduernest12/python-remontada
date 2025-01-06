## Python [flask,django,fastapi] rest backend connected to angular client

### Running the Clients and Backends with Docker Compose
`docker compose up`

### routes
 - https://client.localhost angular client
 - https://flask.localhost flask backend
 - https://fastapi.localhost fastapi backend
 - https://django.localhost django backend

### issues
- 
   

# Lessons

## FastAPI
### Ingredients:
- `main.py`
- Model class
- Pydantic
- Annotations for routes
- Validations
- Manual serialization with comprehensions for `vars(**someClass)` or `someClass.__dict__`
- Manual integration of Alembic for DB migrations
- SQLAlchemy for DB access
- `db.session(SomeModel)` for DB access

### Instructions:
1. Work with `main.py` to set up your FastAPI application.
2. Define your model classes using Pydantic.
3. Use annotations for route definitions.
4. Implement validations as needed.
5. Manually serialize data using comprehensions like `vars(**someClass)` or `someClass.__dict__`.
6. Integrate Alembic manually for database migrations.
7. Use SQLAlchemy for database interactions.
8. Access the database using `db.session(SomeModel)`.

## Django
### Ingredients:
- Django-admin
- Views (controller)
- Models
- Serializers (validation or not)
- URL (routing)
- Settings (app config, CORS, allowed_hosts)

### Instructions:
1. Set up your project with `django-admin startproject [name]`.
2. Organize your files: views, models, serializers, URLs, and settings.
3. Configure your app settings, including CORS and allowed hosts.

## Flask
### Ingredients:
- `main.py`
- Pipenv
- Flask-Alembic for migrations
- Flask-SQLAlchemy
- Flask-Restx for API route handling and OpenAPI autodocs

### Instructions:
1. Create a simple `main.py` file.
2. Use Pipenv for environment management.
3. Integrate Flask-Alembic for database migrations.
4. Use Flask-SQLAlchemy for database interactions.
5. Handle API routes with Flask-Restx, which also provides OpenAPI autodocs.



# Framework Comparison

| Feature               | FastAPI                                                                                         | Django                                                                                          | Flask                                                                                          |
|-----------------------|-------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| Routing               | Annotations for routes                                                                          | URL routing in `urls.py`                                                                        | Route decorators                                                                               |
| Migration             | Manual integration of Alembic                                                                   | Built-in with `manage.py migrate`                                                               | Flask-Alembic                                                                                  |
| Controller Example    | ```python<br>from fastapi import FastAPI<br><br>app = FastAPI()<br><br>@app.get("/")<br>def read_root():<br>    return {"Hello": "World"}<br>``` | ```python<br>from django.http import HttpResponse<br><br>def index(request):<br>    return HttpResponse("Hello, world!")<br>``` | ```python<br>from flask import# Framework Comparison

| Feature               | FastAPI                                                                                         | Django                                                                                          | Flask                                                                                          |
|-----------------------|-------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| Routing               | Annotations for routes                                                                          | URL routing in `urls.py`                                                                        | Route decorators                                                                               |
| Migration             | Manual integration of Alembic                                                                   | Built-in with `manage.py migrate`                                                               | Flask-Alembic                                                                                  |
| Controller Example    | ```python<br>from fastapi import FastAPI<br><br>app = FastAPI()<br><br>@app.get("/")<br>def read_root():<br>    return {"Hello": "World"}<br>``` | ```python<br>from django.http import HttpResponse<br><br>def index(request):<br>    return HttpResponse("Hello, world!")<br>``` | ```python<br>from flask import