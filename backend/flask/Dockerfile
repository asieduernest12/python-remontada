
FROM python:3.9-alpine3.21

WORKDIR /app

RUN pip install pipenv
# COPY requirements.txt requirements.txt
COPY Pipfile Pipfile
# RUN pipenv install -r requirements.txt
RUN pipenv install

COPY . .

CMD ["pipenv","run","flask", "run", "--host=0.0.0.0", "--port=80"]