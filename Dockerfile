FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install pipenv on the container
RUN pip install --upgrade pip
RUN pip install pipenv

# Set the working directory in the container
WORKDIR /app

COPY Pipfile Pipfile.lock ./
COPY requirements.txt ./

# Install project dependency
RUN pipenv install -r requirements.txt

# Copy the current directory contents into the container at /code/
COPY . ./

# Expose the port Django runs on
EXPOSE 8000

# Define the default command to run when the container starts
CMD ["python", "manage.py", "runserver"]