# Use the official Python image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock ./

# Install pipenv on the container
RUN pip install pipenv

# install project dependencies
RUN pipenv install --system

# Copy the Django application code to the container
COPY . .

# Expose the Django development server port
EXPOSE 7072

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:7072"]