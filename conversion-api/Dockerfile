# FROM tiangolo/uvicorn-gunicorn:python3.8

# LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

# COPY ./app /app
# RUN pip install fastapi
# RUN pip install --upgrade pip
# WORKDIR /app


# 
FROM tiangolo/uvicorn-gunicorn:python3.7

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

WORKDIR /code/app

# # 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]


