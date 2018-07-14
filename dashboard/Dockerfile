FROM node:8-alpine

WORKDIR /usr/src/app

COPY package.json ./
COPY package-lock.json ./
RUN npm install --quiet

COPY . ./

EXPOSE 8080
CMD [ "npm", "run", "serve" ]
