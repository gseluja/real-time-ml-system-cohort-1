# The builder image, used to build the virtual environment
FROM python:3.10.3-slim-buster as builder

# stream logs in Docker console
ENV PYTHONUNBUFFERED=1

# add /app/src to PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/app/src"

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Install poetry inside de container
RUN pip install poetry==1.8.3

# Set the working directory
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/

# Install the dependencies from the pyproject.toml to reproduce the environment
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

#----------------------------------------------
  
# The runtime image, used to just run the code provided its virtual environment
FROM python:3.10.3-slim-buster as runtime
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copy all the source code into the container
COPY . /app/

# Run the application
CMD ["poetry", "run", "python", "src/main.py"]
