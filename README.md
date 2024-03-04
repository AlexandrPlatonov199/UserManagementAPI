# User Management API
This project is a simple API created using FastAPI that works with an SQLite database using SQLAlchemy. The API provides CRUD operations for managing users and also offers various data analysis functions.

## Project Goals
- Creating a simple API using FastAPI and SQLAlchemy
- Implementing CRUD operations for users
- Providing data analysis functions to retrieve user information
- Combining all functions into one project
- Writing unit tests and creating documentation

## Main Features
- Create, read, update, and delete users
- Pagination support for retrieving user lists
- Calculating the number of users registered in the last 7 days
- Returning the top 5 users with the longest names
- Determining the proportion of users with a specific email domain
- Predicting the probability of user activity in the next month

## Installation
Clone the repository:
```shell
git clone https://github.com/yourusername/user-api.git
```

Create and activate a virtual environment:
```shell
python3 -m venv .venv

.venv\Scripts\activate - для Windows;

source .venv/bin/activate - для Linux и MacOS.
```

Install the dependencies:

```shell
pip install poetry==1.6.1
```
```shell
poetry install --all-extras
```
Apply migrations:
```shell
python -m app users database migrations apply
```
## Usage
Run the application:
```shell
python -m app users run
```

Open a web browser and navigate to the API documentation page:
http://localhost:8000/docs



## Testing
Run the unit tests using the following command:
```shell
pytest -v
```
## Documentation
The API documentation is available at:


http://localhost:8000/docs