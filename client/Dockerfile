FROM node:18-alpine AS build-env

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build


FROM nginx:alpine

COPY --from=build-env /app/dist/ /usr/share/nginx/html/
COPY ./gespar.crt ./gespar.key /etc/nginx/ssl/
COPY ./nginx.conf /etc/nginx/conf.d/default.conf