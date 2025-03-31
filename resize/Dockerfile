FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential gcc

COPY ./resize/requirements.txt ./

RUN pip install --user -r requirements.txt

COPY ./resize/app ./app

ENV PATH=/root/.local/bin:$PATH

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--workers", "4", "--log-config", "app/log_config.yml", "--reload"]