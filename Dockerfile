FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

RUN pip install pydantic-core

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
