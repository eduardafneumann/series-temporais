FROM nginx:alpine

EXPOSE 80

WORKDIR /app

RUN apk update && \
    apk add --no-cache bash openrc && \
    rm -rf /var/cache/apk/* && \
    mkdir -p /run/openrc && \
    touch /run/openrc/softlevel && \
    rc-status && \
    rc-update add nginx

CMD ["nginx", "-g", "daemon off;"]
