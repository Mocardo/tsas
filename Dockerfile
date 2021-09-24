FROM gcr.io/google.com/cloudsdktool/cloud-sdk:alpine
# Install python/pip
RUN apk add --update --no-cache python3
RUN apk add py3-pip
#
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./main.py" ]
# CMD [ "sh" ]
