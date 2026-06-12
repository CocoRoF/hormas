# Project Execution Guide

This document guides you on how to set up and run the backend (`web`) and frontend (`web-front`) development environments using Docker Compose.

## Prerequisites

Before running the project, please ensure you meet the following requirements.

1.  **Install Docker & Docker Compose**
    * Please install Docker for your system from the [official Docker Desktop download page](https://www.docker.com/products/docker-desktop/). Docker Compose is included with Docker Desktop.

2.  **Project Source Code**
    * Clone the Git repository or download the source code to your local machine.

3.  **Create Environment Variable File (`.env`)**
    * The backend service requires an environment variable file. You must create a `.env` file in the `./backend/web/` path relative to the project root.
    * Fill in the file with the necessary values according to the project's requirements (e.g., database connection strings, API keys, etc.).

    ```
    # Example for backend/web/.env file
    SECRET_KEY=your_secret_key
    DATABASE_URL=your_database_url
    DEBUG=True
    ```

## Project Structure

The basic directory structure for running the project should be as follows:

```
your-project-root/
├── backend/
│   └── web/
│       ├── .env         # << Required file, create manually
│       └── Dockerfile
├── frontend/
│   └── web-front/
│       └── Dockerfile
├── docker-compose.yml   # << The provided file
├── web_entrypoint.sh    # << Backend entrypoint script
└── web_front_entrypoint.sh # << Frontend entrypoint script
```

## How to Run

1.  **Grant Execute Permissions to Entrypoint Scripts**
    * In your terminal (Linux/macOS), run the command below to grant execute permissions to the `entrypoint.sh` files.
    ```bash
    chmod +x web_entrypoint.sh
    chmod +x web_front_entrypoint.sh
    ```

2.  **Build and Run Docker Containers**
    * From the project's root directory (where the `docker-compose.yml` file is located), run the following command.
    ```bash
    docker-compose up --build
    ```
    * The command above will build (or rebuild) the Docker images and start the containers in foreground mode. Logs will be streamed to your terminal.
    * To run the containers in the background, add the `-d` (detached) option:
    ```bash
    docker-compose up -d --build
    ```

3.  **Verify Execution**
    * **Frontend**: Open your web browser and navigate to `http://localhost:3000` to see if the application is displayed correctly.
    * **Backend**: Navigate to `http://localhost:8000` (or a specific API endpoint) to check if the service is responding.

## Useful Docker Compose Commands

* **Stop and Remove Containers**
    ```bash
    docker-compose down
    ```

* **View Real-time Logs**
    ```bash
    docker-compose logs -f
    ```
    * To view logs for a specific service, add the service name:
    ```bash
    docker-compose logs -f web
    docker-compose logs -f web-front
    ```

* **Access a Running Container**
    * To access the backend container:
    ```bash
    docker-compose exec web bash
    ```
    * To access the frontend container:
    ```bash
    docker-compose exec web-front sh
    ```