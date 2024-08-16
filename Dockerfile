FROM python:3.12

# Core Python Script
ADD main.py .
ADD modules/Scryfall.py .
ADD modules/Palworld.py .


# Python Libraries
ADD requirements.txt .

# Documentation
ADD documentation.md .

# Pictures / Assets
ADD Palworld_Type_Chart.png .

# Discord Credentials
ADD .credentials.txt .

# Update the Docker Container
RUN apt-get update -y

# Install Dependencies
RUN pip install -r requirements.txt

# Start the bot
CMD ["python3", "main.py"]
