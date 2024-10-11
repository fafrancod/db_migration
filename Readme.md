# FastAPI SQL Data Analysis API

This project is an API built with **FastAPI** that allows data analysis on a dataset of employees, departments, and jobs. The API processes CSV files and performs SQL queries to extract insights such as the number of employees hired per quarter for each job and department, and departments that hired above the average.

## Features

- **CSV Uploads**: Upload CSV files containing data for employees, departments, and jobs.
- **SQL Data Analysis**: Provides endpoints to perform SQL queries on the data.
  - **/employees-hired-by-quarter/**: Get the number of employees hired for each job and department in 2021, divided by quarter.
  - **/departments-hiring-above-average/**: List the departments that hired more employees than the average in 2021.
- **Logging and Error Handling**: Proper logging of actions and error handling to ensure smooth operations.

## Requirements

To run this project, you will need:
- **Docker**: Docker is used to containerize the FastAPI application and PostgreSQL database.
- **Python 3.9+**

## Setup Instructions

### 1. Clone the repository

git clone <repository-url>
cd fastapi-db-migration


### 2. Build and Run Docker Containers
The application is containerized using Docker. To run the project:


docker-compose up --build
This will:

Build and start a PostgreSQL database.
Start the FastAPI application.
Access the API on: http://localhost:8000

### 3. Testing the API
The API includes Swagger documentation, which allows you to test the endpoints interactively. Open your browser and navigate to:

http://localhost:8000/docs
This will bring up the Swagger UI where you can interact with the API.

## Endpoints
### 1. Upload CSVs
http
Copy code
POST /upload-csv/
Upload three CSV files:

employees_file: Contains employee data.
departments_file: Contains department data.
jobs_file: Contains job data.
Example:


curl -X 'POST' \
  'http://localhost:8000/upload-csv/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'employees_file=@hired_employees.csv;type=text/csv' \
  -F 'departments_file=@departments.csv;type=text/csv' \
  -F 'jobs_file=@jobs.csv;type=text/csv'


### 2. Employees Hired by Quarter

GET /employees-hired-by-quarter/
Returns the number of employees hired for each department and job, divided by quarter, for the year 2021.

Example Output:

json
Copy code
[
  {
    "department": "Support",
    "job": "Technician",
    "Q1": 10,
    "Q2": 15,
    "Q3": 7,
    "Q4": 8
  },
  ...
]

### 3. Departments Hiring Above Average

GET /departments-hiring-above-average/
Lists the departments that hired more employees than the average for 2021, ordered by the number of employees hired.

Example Output:

json
Copy code
[
  {
    "id": 8,
    "department": "Support",
    "hired": 221
  },
  ...
]


### 4. Test Database Connection

GET /test-db-connection
A simple endpoint to test the database connection.

## Error Handling
Returns 404 if no data is found for the requested year or department.
Returns 500 in case of any internal server error during query execution.

## Logging
All critical operations, such as database queries, uploads, and error handling, are logged for better debugging and monitoring.

## Development
Setting up the Environment Locally
If you'd like to run this project locally without Docker, follow these steps:

## Create a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the dependencies:


pip install -r requirements.txt
Create a .env file to store your database credentials, similar to the example below:


DATABASE_URL="postgresql://postgres:password@localhost:5432/mydatabase"
Run the FastAPI server locally:

uvicorn app.main:app --reload

## Deployment
Note: The project is not currently deployed on Azure or any cloud service. Below are the steps to deploy when needed.

Deployment to Azure (Optional)
Install the Azure CLI.
Login using the Azure CLI.
Push your Docker image to Azure Container Registry (ACR) or any other registry.
Create an Azure Web App for Containers and point it to your Docker image.

## Contributing
Fork the project.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature-branch).
Open a Pull Request.