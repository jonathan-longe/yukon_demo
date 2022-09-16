FROM python:3.7.3-stretch
ARG ADMIN_USERNAME

COPY database_api/requirements.txt /tmp/

RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY common /home/appuser/python/common
COPY database_api /home/appuser/python/database_api

ENV PYTHONPATH /home/appuser/

RUN ["python", "-m", "pytest"]

ENV FLASK_APP /home/appuser/python/database_api

RUN ["flask", "rsbc", "create_db"]

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "--pythonpath", "/home/appuser/python/database_api", "wsgi:create_app()" ]