FROM ubuntu:19.10 

# Environment variables
ENV APP_DIR /app
ENV PYTHONPATH ${APP_DIR}/
ENV LANG=en_US.UTF-8

# Install dependencies and cleanup
RUN apt-get update
RUN apt-get -y install python3-pip git 
RUN pip3 install pylint psutil pytest

# Copy app and set workdir
RUN mkdir -p ${APP_DIR}/resources
WORKDIR ${APP_DIR}
COPY *.py ${APP_DIR}/

# Check syntax
RUN pylint --disable=C  main.py


CMD ["python3", "main.py"]

