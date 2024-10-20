FROM debian:12

RUN apt update && apt install -y python3 python3-pip openssl libssl-dev

COPY requirements.txt /root
RUN pip3 install --break-system-packages -r /root/requirements.txt

COPY dist /root/dist
COPY 2024.pub /root
COPY app.py /root
COPY logger.py /root
COPY flag.py /root
COPY sql.py /root
COPY ratelimit.py /root

WORKDIR /root
CMD ["python3", "-u", "/root/app.py"]
EXPOSE 8000

