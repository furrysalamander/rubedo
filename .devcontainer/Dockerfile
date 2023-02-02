FROM debian:bullseye-slim

# RUN apk add --no-cache make automake gcc g++ subversion python3-dev
# RUN apk add --no-cache python3 py3-pip
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install opencv-python-headless
# RUN pip3 install --upgrade pip setuptools wheel
# RUN pip3 install opencv-python
# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
