# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /school_app

# COPY requirements file
COPY requirements.txt /school_app/
# Copy the current directory contents into the container at /app
COPY . /school_app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
#ENV NAME APP_NAME

# Collect static files
RUN python manage.py collectstatic --noinput

# Run app.py when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "school_app.wsgi.application"]

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]