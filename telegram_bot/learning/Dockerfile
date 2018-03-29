FROM ubuntu

RUN apt-get update && apt-get -y upgrade
RUN apt-get install openssl -y

RUN mkdir /ssl_sertificate
VOLUME ./ssl_sertiicate:/ssl_sertificate

RUN echo '123' > /ssl_sertificate/asd
RUN cat /ssl_sertificate/asd

# сгенерируем ключик
#RUN openssl genrsa -out /ssl_sertificate/webhook_pkey.pem 2048
## генерируем сертификат ключом
#RUN openssl req -new -x509 -days 3650 -key /ssl_sertificate/webhook_pkey.pem -out webhook_cert.pem