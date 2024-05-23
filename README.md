# HR Application

## Overview

This HR application is designed to handle a wide range of human resources tasks including user authentication, automated email and phone confirmations, question and answer forums, and more. It automatically manages database schemas and tables, and serves static files from specified directories.

## Features

- **User Authentication**: Secure login and registration system.
- **Email and Phone Confirmation**: Automatic verification mechanisms for user accounts.
- **Q&A Forum**: Allows users to ask and answer questions related to HR topics.
- **Automatic DB Schema Management**: Automatically creates and manages database schemas and tables.
- **Static File Serving**: Dynamically serves static files from designated directories.

## Technology Stack

- **FastAPI**: High-performance web framework for building APIs.
- **Uvicorn**: ASGI server for serving the FastAPI application.
- **MySQL**: Database system for storing all user and application data.

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Google Email Application](https://support.google.com/mail/answer/185833?hl=en)
- [Zadarma Service](https://zadarma.com/en/)

### Clone the Repository

```bash
git clone https://github.com/darkbrains/hr-app.git
cd hr-app
```

### Environment Setup

Create a .env file at the root of the project directory with the necessary variables:

```plaintext
EMAIL_ADDRESS=<your-email-app-address>
EMAIL_PASSWORD=<your-email-app-password>
MYSQL_ROOT_PASSWORD=<your-mysql-root-password>
MYSQL_DB=<your-database-name>
MYSQL_USER=<your-mysql-user>
MYSQL_PASSWORD=<your-mysql-password>
ZADARMA_API_KEY=<your-zadarma-api-key>
ZADARMA_API_SECRET=<your-zadarma-api-secret>
```

### Docker Compose
Here's a sample docker-compose.yml that configures both the application and MySQL services:

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8085:8085"
    environment:
      - EMAIL_ADDRESS=${EMAIL_ADDRESS}
      - EMAIL_PASSWORD=${EMAIL_PASSWORD}
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      - MYSQL_DB=${MYSQL_DB}
      - MYSQL_USER=${MYSQL_USER}
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
      - ZADARMA_API_KEY=${ZADARMA_API_KEY}
      - ZADARMA_API_SECRET=${ZADARMA_API_SECRET}
    depends_on:
      - db
  db:
    image: mysql:5.7
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    ports:
      - "3306:3306"
    volumes:
      - db-data:/var/lib/mysql
volumes:
  db-data:
```

### Building and Running the Application

Execute the following command to build and start your application using Docker Compose:

```bash
docker-compose up --build
```

### Access from the browser

After the application is running, access the FastAPI built-in Swagger UI to view and interact with the available endpoints:

```bash
http://localhost:8085/
```
