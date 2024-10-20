FROM debian:12

RUN apt update && apt install -y python3 python3-pip
COPY requirements.txt /root
RUN pip install --break-system-packages -r /root/requirements.txt

WORKDIR /root
COPY dinic.cpp /root
COPY spfa.cpp /root
RUN g++ spfa.cpp -o spfa -O2 -std=c++17
RUN g++ dinic.cpp -o dinic -O2 -std=c++17

COPY server.py /root
COPY logger.py /root
COPY templates /root/templates
COPY static /root/static

CMD ["/usr/bin/python3", "-u", "/root/server.py"]
