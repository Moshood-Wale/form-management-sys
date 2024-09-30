# Form Management System API

This project is a Form Management System API built with Django Rest Framework and MongoDB. It allows users to create, manage, and submit responses to custom forms.

## Features

- Create, read, update, and delete forms
- Submit responses to forms
- Retrieve form responses
- Basic form analytics
- API documentation with Swagger/OpenAPI

## Prerequisites

- Docker
- Docker Compose
- MongoDB Atlas account

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/Moshood-Wale/form-management-sys.git
   cd form-management-sys
   ```

2. Create a `.env` file in the project root and add the environment variables specified in .env.sample:

   Replace the values with your actual MongoDB Atlas credentials:
   - `MONGODB_USERNAME`: Your MongoDB Atlas database user
   - `MONGODB_PASSWORD`: Your MongoDB Atlas database password
   - `MONGODB_CLUSTER`: Your MongoDB Atlas cluster URL (e.g., cluster0.abcde.mongodb.net)
   - `MONGODB_NAME`: The name of your database

3. Ensure your MongoDB Atlas cluster is set up:
   - Create a cluster in MongoDB Atlas if you haven't already
   - In the MongoDB Atlas dashboard, go to "Network Access" and add your current IP address to the IP Whitelist
   - In "Database Access", create a database user with read and write permissions

4. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

   This command will build the Docker image and start the containers for the Django application.

5. The API should now be running at `http://localhost:8000`.

## API Documentation

Once the server is running, you can access the API documentation:

- Swagger UI: `http://127.0.0.1:8000/api/v1/doc/#/`

## Usage

Here are some example API endpoints:

- List all forms: GET `/api/forms/`
- Create a new form: POST `/api/forms/`
- Retrieve a specific form: GET `/api/forms/{form_id}/`
- Update a form: PUT `/api/forms/{form_id}/`
- Delete a form: DELETE `/api/forms/{form_id}/`
- Submit a response to a form: POST `/api/forms/{form_id}/submit/`
- Get responses for a form: GET `/api/forms/{form_id}/responses/`
- Get form analytics: GET `/api/forms/{form_id}/analytics/`

For detailed information on request/response formats, please refer to the API documentation.

## Troubleshooting

If you encounter any issues with database connections, ensure that:
- Your MongoDB Atlas cluster is running and accessible.
- The IP address of your Docker container is whitelisted in MongoDB Atlas Network Access settings.
- The credentials in your `.env` file are correct.

For any persistent issues, check the Django server logs for more detailed error messages:
```
docker-compose logs api
```