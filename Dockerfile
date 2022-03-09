#FROM python:3.8-slim-buster
#FROM ubuntu
FROM apache1
WORKDIR /var/www/html
COPY servicestart.sh servicestart.sh
CMD [ "./servicestart.sh"]


