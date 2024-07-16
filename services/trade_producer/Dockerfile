# Base image used to build the container
FROM python:3.10.3-slim-buster

# stream output to console
ENV PYTHONUNBUFFERED=1

# add /app/src to PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/app/src"

# Install poetry inside de container
RUN pip install poetry==1.8.3

# Set the working directory
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/

# Install the dependencies from the pyproject.toml to reproduce the environment
RUN poetry install

# Copy all the source code into the container
COPY . /app/

# Run the application
CMD ["poetry", "run", "python", "src/main.py"]
