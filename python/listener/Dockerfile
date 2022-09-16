FROM python:3.7.3-stretch

COPY listener/requirements.txt /tmp/

RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

ENV PYTHONPATH /home/appuser/

COPY common /home/appuser/python/common
COPY listener /home/appuser/python/listener

# RUN ["python", "-m", "pytest"]

CMD [ "python", "./python/listener/listener.py" ]
