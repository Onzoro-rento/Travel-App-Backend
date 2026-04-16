
FROM python:3.14


WORKDIR /src

COPY ./requirements.txt /src/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt


COPY ./app /src/app


CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]