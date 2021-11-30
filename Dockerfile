FROM gcr.io/google.com/cloudsdktool/cloud-sdk:slim
ENV GOOGLE_APPLICATION_CREDENTIALS="/usr/src/app/secrets/csi-02-tsas-b3813428de3e.json"

# Install python/pip
RUN apt update
RUN apt upgrade -y
RUN apt install python3
RUN apt install python3-pip
#

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
# Due to grpcio package to upgrade pip
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade google-cloud-language

COPY . .
CMD [ "python3", "./main.py" ]
