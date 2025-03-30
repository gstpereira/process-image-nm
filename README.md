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
    - Username: `guest`
    - Password: `guest`

- **MinIO**:
  - MinIO is a high-performance, S3-compatible object storage system. It is used to store and retrieve files in a scalable and efficient manner.
  - Console: [http://localhost:9001](http://localhost:9001)
  - Default credentials:
    - Access Key: `minioadmin`
    - Secret Key: `minioadmin`

### Stopping the Services

To stop the services, run:

```bash
docker-compose down
```

### Notes

- Ensure that the ports `15672` (RabbitMQ) and `9001` (MinIO) are not in use by other applications.
- You can customize the configuration by editing the `docker-compose.yml` file.
