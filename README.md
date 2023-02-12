# Marvel-backend
This is a Flask-based backend for the Marvel application. It uses MongoDB as the database and is contained within a Docker container for ease of deployment.

## Getting Started
These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites
Before you begin, you will need to have the following software installed on your machine:

- Docker
- Python 3
- pip

## Installing
1. Clone this repository:
```bash
git clone https://github.com/guillermoreyesv/Marvel-backend.git
```

2. Navigate to the repository directory:
```bash
cd Marvel-backend
```

3. Copy the .env.example file to .env:
```bash
cp .env.example .env
```
4. Open the .env file and update the values to match your environment.

### Using docker
5. Build the Docker container:
```bash
docker build -t marvel-backend .
```

6. Run the container:
```bash
docker run -d -p 5000:5000 --name marvel-container marvel-image
```

### In local

5. Install the required packages:
```python
pip install --no-cache-dir -r requirements.txt
```

6. Start the application:
```bash
python run.py
```

7. Your Marvel-backend should now be up and running!

## Deployment
To deploy this application to a production environment, you will need to follow the steps above, making any necessary modifications to match your environment.

## Built With
- <ins>Flask</ins> - A lightweight Python web framework.
- <ins>MongoDB</ins> - A NoSQL document-oriented database.
- <ins>Docker</ins> - A platform for building and deploying applications in containers.