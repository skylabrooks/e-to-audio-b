#!/bin/bash
echo "Starting EtoAudioBook Docker Deployment..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if credentials file exists
if [ ! -f "Backend/credentials/service-account.json" ]; then
    echo "Error: Google Cloud service account credentials not found."
    echo "Please place your service-account.json file in Backend/credentials/"
    exit 1
fi

# Stop existing containers
echo "Stopping existing containers..."
docker-compose down

# Build and start containers
echo "Building and starting containers..."
docker-compose up --build -d

# Wait for services to start
echo "Waiting for services to start..."
sleep 10

# Check container status
echo "Checking container status..."
docker-compose ps

echo ""
echo "Deployment complete!"
echo "Frontend: http://localhost"
echo "Backend API: http://localhost:5000"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"