FROM python:3.6.5

RUN apt-get update && apt-get install -y postgresql-client

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pip install pipenv
RUN pipenv install --system --dev

RUN groupadd -r uskpa && useradd --no-log-init -r -g uskpa uskpa
USER uskpa