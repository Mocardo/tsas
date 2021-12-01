FROM gcr.io/google.com/cloudsdktool/cloud-sdk:slim
WORKDIR /usr/src/app

# Install python/pip
RUN apt update
RUN apt upgrade -y
RUN apt install python3
RUN apt install python3-pip

# Install python dependencies
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
# Due to grpcio package to upgrade pip
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade google-cloud-language


# Congure environment variables
ARG GOOGLE_SECRET_FILE
ARG TWITTER_SECRET_FILE
ENV GOOGLE_SECRET_FILE=$GOOGLE_SECRET_FILE
ENV TWITTER_SECRET_FILE=$TWITTER_SECRET_FILE
RUN mkdir secrets
RUN echo $GOOGLE_SECRET_FILE > ./secrets/google_application_credentials.json
RUN echo $TWITTER_SECRET_FILE > ./secrets/twitter_api_key.json

ENV GOOGLE_APPLICATION_CREDENTIALS="/usr/src/app/secrets/google_application_credentials.json"

# Run the app
COPY . .
CMD ["gunicorn", "app:app"]
