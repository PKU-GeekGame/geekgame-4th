FROM debian:12

RUN apt update && apt install -y python3 python3-pip
COPY requirements.txt /root
RUN pip3 install --break-system-packages -r /root/requirements.txt

COPY flask_compress.py /root
COPY flag.py /root
COPY logger.py /root
COPY 2024.pub /root
COPY chal_server.py /root
COPY static /root/static
COPY templates /root/templates

WORKDIR /root
CMD ["/usr/bin/python3", "-u", "/root/chal_server.py"]
