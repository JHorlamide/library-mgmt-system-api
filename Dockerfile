# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# # Install pipenv on the container
RUN pip install --upgrade pip
RUN pip install pipenv

# Set the working directory in the container
WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

# RUN pipenv requirements > requirements.txt
# COPY ./requirements.txt ./requirements.txt 
# RUN chmod +x ./requirements.txt
# RUN pipenv install -r requirements.txt

# Copy the current directory contents into the container at /code/
COPY . ./

# Expose the port Django runs on
EXPOSE 8000

# Define the default command to run when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# # Use the official Python image as the base image
# FROM python:3.9

# # Install pipenv on the container
# RUN pip install --upgrade pip
# RUN pip install --upgrade pipenv

# # Set the working directory inside the container
# WORKDIR /app

# # Copy the Pipfile and Pipfile.lock to the container
# COPY Pipfile Pipfile.lock ./

# ENV PYTHONUNBUFFERED=1

# # install project dependencies
# RUN pipenv install --system --dev

# # Copy the Django application code to the container
# COPY . .

# # Start the Django development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]