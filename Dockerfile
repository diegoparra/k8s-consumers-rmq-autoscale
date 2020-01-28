FROM python:3.7-alpine

# Install dependencies - if they don't change, we can keep the cached layer
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip; pip install -r requirements.txt

# Get the app
COPY src /src
WORKDIR /