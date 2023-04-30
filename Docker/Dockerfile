# Use the official Python image as the base image
FROM --platform=linux/amd64 python:3.11.2-alpine3.17

# Set the working directory
WORKDIR /src

# Copy the requirements file into the container
COPY ./Discord_bot/requirements.txt ./

RUN apk update
RUN apk upgrade

# Install the Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for the Discord token and OpenAI API key
ARG DISCORD_TOKEN
ENV DISCORD_TOKEN=${DISCORD_TOKEN}
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Copy the rest of the application code into the container
COPY ./Discord_bot/src .

# Run the application
CMD ["/usr/local/bin/python", "bot.py"]
