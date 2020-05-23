FROM nikolaik/python-nodejs:python3.8-nodejs14

COPY scripts/wait-for-it.sh /
RUN chmod 755 wait-for-it.sh
WORKDIR /gui
COPY gui/package.json .
RUN npm install --silent
RUN npm install react react-dom react-router-dom bootstrap --silent
COPY gui/ /gui
RUN npm run build
WORKDIR /
COPY requirements.txt /
RUN pip3.8 install -r requirements.txt
COPY thinkpol /thinkpol

