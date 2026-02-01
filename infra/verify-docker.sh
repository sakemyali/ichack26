#!/bin/bash

# Docker Setup Verification Script
# This script checks if Docker is set up correctly before building

echo "=========================================="
echo "Docker Setup Verification"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "   Install Docker Desktop from: https://www.docker.com/products/docker-desktop"
    exit 1
else
    echo "✅ Docker is installed: $(docker --version)"
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    echo "   Docker Compose should come with Docker Desktop"
    exit 1
else
    echo "✅ Docker Compose is installed: $(docker-compose --version)"
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon is not running"
    echo "   Please start Docker Desktop and try again"
    exit 1
else
    echo "✅ Docker daemon is running"
fi

# Check if .env file exists
if [ ! -f ../middleware/.env ]; then
    echo "⚠️  Warning: ../middleware/.env not found"
    echo "   Create it with your Copernicus credentials:"
    echo "   CDSE_CLIENT_ID=your-client-id"
    echo "   CDSE_CLIENT_SECRET=your-client-secret"
else
    echo "✅ Middleware .env file exists"
fi

echo ""
echo "=========================================="
echo "Ready to build and run!"
echo "=========================================="
echo ""
echo "To build and start all services:"
echo "  cd infra && docker-compose up --build"
echo ""
echo "To build a single service:"
echo "  docker-compose build middleware"
echo "  docker-compose build backend"
echo ""
echo "To start in background:"
echo "  docker-compose up -d --build"
echo ""
