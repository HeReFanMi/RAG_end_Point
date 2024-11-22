
# RAG System

## Overview
The RAG (Retrieval-Augmented Generation) system is a core component of the HereFamni project. It integrates retrieval and generation capabilities to address the detection of healthcare-related fake news. By leveraging a database of vector embeddings, the RAG model retrieves relevant content and generates responses augmented by this information.

## Features
- Retrieves context-relevant information from a knowledge base.
- Generates responses enriched with retrieved information.
- Exposes API endpoints for integration with external systems.

## Setup Instructions

### Prerequisites
- Docker and Docker Compose installed.
- A running PostgreSQL database container (configured separately).

### Steps
1. **Clone the repository**:
    ```bash
    git clone https://github.com/HeReFanMi/Rag.git
    cd Rag
    ```

2. **Build and Run the Docker Container**:
    Build the Docker image and start the containers:
    ```bash
    docker build -t ragystem-flask-app .
    docker-compose up
    ```

3. **Access the Application**:
    Once the containers are running, access the API at:
    ```bash
    http://localhost:5000
    ```

## API Endpoints

### POST /find_similar_chunks
**Description**: Retrieve similar content chunks from the knowledge base.

**Request Body**:
```json
{
  "query": "Your query string here"
}
```

**Response**:
```json
{
  "results": [
    {"chunk_id": 1, "content": "Sample content", "score": 0.9},
    ...
  ]
}
```

## Environment Variables
The following environment variables are used to configure the system:

- `DB_HOST`: Hostname or IP address of the database.
- `DB_PORT`: Port number for the database (default: `5432`).
- `DB_USER`: Username for database access.
- `DB_PASSWORD`: Password for database access.
- `DB_NAME`: Database name.

## Network Configuration
Ensure that the `ragystem_shared-network` Docker network is used for communication between containers. Verify it using:
```bash
docker network inspect ragystem_shared-network
```

## Contributing
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes and open a pull request.

## License
This project is licensed under the MIT License.
