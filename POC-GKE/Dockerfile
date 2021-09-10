FROM python:3

# Creating and setting WORKDIR
RUN mkdir /TweetsApp
WORKDIR /TweetsApp

#Copying files from host
COPY . /TweetsApp/

# Install Gsutil
RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin

# Gsutil Auth
RUN bash gsutil_auth.sh

# Install requirements for python application
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "tweetsApp.py" ]