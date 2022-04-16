FROM node:17.8.0-alpine
RUN npm install -g http-server
COPY . /front
WORKDIR /front
RUN npm install
RUN npm run build
CMD node server.js