FROM python:3.12

RUN mkdir /app

COPY run /app
COPY service.py /app

RUN chmod +x /app/run
RUN echo "fake{flag1}" /app/flag1.txt
RUN echo "fake{flag2}" /app/flag2.txt

RUN adduser guest
USER guest

WORKDIR /app
CMD [ "python3", "-u", "service.py" ]
