FROM python:3.12

# Copy Files
COPY . .

# Update the Docker Container
RUN apt-get update -y

# Install Dependencies
RUN pip install -r requirements.txt

# Start the bot
CMD ["python3", "main.py"]
