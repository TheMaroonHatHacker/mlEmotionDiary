FROM python:3.9.19-slim-bookworm
RUN apt-get update -y
RUN apt-get install build-essential -y
WORKDIR /ml/
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY models ./models
RUN cd models/ && python3 generateModel.py
COPY . .
CMD uvicorn fastApi:app --host 0.0.0.0 --port 8080 --workers 4