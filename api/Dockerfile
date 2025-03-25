FROM python:3.12
WORKDIR /app
COPY ["/api/requirements.txt", "/app/"]
RUN pip install -r requirements.txt
COPY ["/api/", "/app/"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]