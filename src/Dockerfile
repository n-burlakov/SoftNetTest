FROM python:3.11.0-alpine

WORKDIR ./app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .app/requirements.txt

# install dependencies
RUN pip install --upgrade pip setuptools wheel && pip install -r .app/requirements.txt && rm -rf /root/.cache/pip

COPY ../.. .

#CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]