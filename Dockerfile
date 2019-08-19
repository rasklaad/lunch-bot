FROM python:3.6.9
ENV PIPENV_VENV_IN_PROJECT=true
WORKDIR /root
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pip3 install pipenv && pipenv install Pipfile
