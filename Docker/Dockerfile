# Use the official Python image as the base image
FROM python:latest

# Set the working directory
WORKDIR /src

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for the Discord token and OpenAI API key
ARG DISCORD_TOKEN
ENV DISCORD_TOKEN=${DISCORD_TOKEN}
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Copy the rest of the application code into the container
COPY . .

# Run the application
CMD ["python", "run.py"]
