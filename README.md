# Librarian

Librarian is a web application for managing books in a library.

## Getting Started

### Prerequisites

- Docker: Make sure Docker is installed on your machine.

### Installation and Setup

1. Clone the repository:
   ```bash
   git clone git@github.com:sankarme001/Librarian.git
   cd Librarian

2. Build and Run
-- Kill Port 5432
-- Kill port 5432 if it's already in use:

    sudo kill -9 $(sudo lsof -t -i:5432)

3. Build Docker Images
-- Build the Docker images and start the containers:

    docker-compose up --build

4. Run Docker Containers
-- If the images are already built and you just want to start the containers:

    docker-compose up

5. to run the application

    uvicorn main:app --host localhost --port 8000 --reload --debug 


