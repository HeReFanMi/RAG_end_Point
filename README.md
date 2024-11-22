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
1. Clone the repository:
   ```bash
git clone https://github.com/HeReFanMi/Rag.git
cd Rag


2. Build and Run the Docker Container
Build the Docker image and start the containers
   ```bash
docker build -t ragystem-flask-app .
docker-compose up
3.Access the Application
   ```bash
http://localhost:5000
