FROM nginx:1.27-alpine

RUN rm -rf /usr/share/nginx/html/*

COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/
COPY script.js /usr/share/nginx/html/
COPY ressources /usr/share/nginx/html/ressources

EXPOSE 80