#!/bin/bash

# Set the URLs for your repositories
REPOS=(
  "https://github.com/yourusername/RAG_end_Point.git"
  "https://github.com/yourusername/NGI_LLM.git"
  "https://github.com/yourusername/Docker-compose.git"
  "https://github.com/yourusername/Backend.git"
  "https://github.com/yourusername/Frontend.git"
  "https://github.com/yourusername/Vector_DB.git"
)

# Directory to clone repos into
WORK_DIR="$HOME/projects"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# Clone all repositories
for REPO_URL in "${REPOS[@]}"; do
  REPO_NAME=$(basename "$REPO_URL" .git)
  if [ ! -d "$REPO_NAME" ]; then
    echo "Cloning $REPO_NAME..."
    git clone "$REPO_URL"
  else
    echo "$REPO_NAME already exists. Pulling the latest changes..."
    cd "$REPO_NAME"
    git pull origin main  # Replace 'main' with 'master' or your default branch if needed
    cd "$WORK_DIR"
  fi
done

# Navigate to the main directory containing the docker-compose.yml and start containers
cd "$WORK_DIR/Docker-compose"  # Adjust the path if your main docker-compose file is elsewhere

echo "Starting containers with docker-compose..."
docker-compose -f docker-compose.yml up --build
