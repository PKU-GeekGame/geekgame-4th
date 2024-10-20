FROM ghcr.io/usememos/memos:latest

RUN apk add --no-cache sqlite
COPY init.sh /init.sh
RUN chmod +x /init.sh
COPY memos_prod.db /tmp/memos_prod.db
COPY memos /usr/local/memos/memos
ENTRYPOINT [ "/init.sh" ]
