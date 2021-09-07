FROM python:3

# Creating and setting WORKDIR
RUN mkdir /TweetsApp
WORKDIR /TweetsApp

#Copying files from host
COPY . /TweetsApp/

# Install AWS cli
RUN pip install awscli

# Config AWS Cli
RUN bash aws_config.sh

# Install requirements for python application
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "tweetsApp.py" ]