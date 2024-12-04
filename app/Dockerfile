FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu20.04

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip3 install --no-cache-dir flask torch torchvision torchaudio

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]
