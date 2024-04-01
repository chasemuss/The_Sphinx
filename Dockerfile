FROM python:3.12

# Core Python Script
ADD main.py .
#ADD scryfall.py .
#ADD Palworld.py .


# Python Libraries
ADD requirements.txt .

# Documentation
ADD documentation.md .

# Pictures / Assets
ADD freddy.gif .
ADD cringe.gif .
ADD Palworld_Type_Chart.png .

# Update the Docker Container
#RUN apt-get update -y
#RUN apt-get install -y iputils-ping

# Install Dependencies
RUN pip install -r requirements.txt

# Start the bot
CMD ["python3", "main.py"]
