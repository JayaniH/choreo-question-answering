# syntax=docker/dockerfile:1

# FROM python:3.8-alpine
FROM ufoym/deepo:keras-py38-cpu

WORKDIR /choreo-question-answering

# RUN apk --update add gcc build-base freetype-dev libpng-dev openblas-dev
#
# RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# ENV PATH="/root/.cargo/bin:${PATH}"

COPY docker-images/requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

RUN ls
USER 10016
EXPOSE 5005

# CMD [ "flask", "run", "--host=0.0.0.0", "--port=5005"]

COPY docker-images/entrypoint.sh .

EXPOSE 5005

ENTRYPOINT ["/bin/bash","entrypoint.sh"]