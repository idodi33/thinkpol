FROM python:3.8-slim-buster
COPY requirements.txt /
RUN pip3.8 install -r requirements.txt
COPY scripts/wait-for-it.sh /
RUN chmod 755 wait-for-it.sh
COPY thinkpol /thinkpol
