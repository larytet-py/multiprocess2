FROM ubuntu:19.10 

# Environment variables
ENV APP_DIR /app
ENV PYTHONPATH ${APP_DIR}/
ENV LANG=en_US.UTF-8

# Install dependencies and cleanup
RUN apt-get update \
    && apt-get -y install python3-pip  \
    && apt-get -y install curl \
    && apt-get -y install git 

# Copy app and set workdir
RUN mkdir -p ${APP_DIR}/resources
WORKDIR ${APP_DIR}
COPY *.py ${APP_DIR}/

# Check syntax
RUN pylint --disable=R,C,W  extract_url.py service.py


CMD ["python3", "service.py"]

