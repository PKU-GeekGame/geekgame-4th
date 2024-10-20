FROM debian:12

RUN apt update && apt install -y fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 unzip xvfb curl python3 python3-pip
RUN curl https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_129.0.6668.70-1_amd64.deb -o /usr/src/google-chrome.deb && \
    apt install /usr/src/google-chrome.deb -y -f && \
    rm /usr/src/google-chrome.deb
RUN curl https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.70/linux64/chromedriver-linux64.zip -o /usr/src/chromedriver-linux64.zip && \
    unzip /usr/src/chromedriver-linux64.zip -d /usr/src && \
    cp /usr/src/chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver

RUN apt install -y mitmproxy

COPY requirements.txt /root
RUN pip3 install --break-system-packages -r /root/requirements.txt

COPY flag_server.py /root
COPY hacker_server.py /root
COPY xssbot.py /root
COPY bxx-extension.zip /root
RUN unzip -d /root /root/bxx-extension.zip

WORKDIR /root
CMD ["/usr/bin/python3", "-u", "/root/xssbot.py"]
