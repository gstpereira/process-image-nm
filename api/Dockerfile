FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential gcc

COPY ./api/requirements.txt ./

RUN pip install --user -r requirements.txt

COPY ./api/app ./app

ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]