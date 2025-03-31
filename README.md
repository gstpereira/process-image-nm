# Process Image NM

## Running the Project with Docker Compose

This project uses Docker Compose to orchestrate its services, including RabbitMQ and MinIO. Follow the steps below to get started:

### Prerequisites

- Ensure you have Docker and Docker Compose installed on your system.

### Steps to Run

1. Clone the repository:

   ```bash
   git clone git@github.com:gstpereira/process-image-nm.git
   cd process-image-nm
   ```

2. Start the services using Docker Compose:

   ```bash
   docker compose up -d
   ```

3. Verify that the services are running:
   ```bash
   docker compose ps
   ```

### Services and URLs

- **RabbitMQ**:

  - Management UI: [http://localhost:15672](http://localhost:15672)
  - Default credentials:
    - Username: `user`
    - Password: `pass`

- **MinIO**:

  - MinIO is a high-performance, S3-compatible object storage system. It is used to simulate S3 storage for this project. Uploaded images are stored here, and resized images are also saved for retrieval.
  - Console: [http://localhost:9001](http://localhost:9001)
  - Default credentials:
    - Access Key: `MINIOACCESSKEY`
    - Secret Key: `MINIOSECRETKEY`

- **FastAPI**:
  - FastAPI provides an interactive API documentation where you can test endpoints, including uploading an image for processing. Once an image is uploaded, FastAPI processes it, resizes it, and returns a URL pointing to the resized image stored in MinIO.
  - Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

### Stopping the Services

To stop the services, run:

```bash
docker-compose down
```

### Notes

- Ensure that the ports `15672` (RabbitMQ) and `9001` (MinIO) are not in use by other applications.
- You can customize the configuration by editing the `docker-compose.yml` file.
