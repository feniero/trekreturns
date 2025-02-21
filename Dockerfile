FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry==2.1.1 && poetry install --no-root

COPY . .

EXPOSE 8900

ENTRYPOINT ["poetry", "run", "streamlit", "run", "./trekreturns/main.py", "--server.port=8900", "--server.address=0.0.0.0"]
