FROM debian:12

# BELOW are only required for challenge 1

RUN apt update && apt install -y fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 unzip xvfb curl python3 python3-pip
RUN curl https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_129.0.6668.70-1_amd64.deb -o /usr/src/google-chrome.deb && \
    apt install /usr/src/google-chrome.deb -y -f && \
    rm /usr/src/google-chrome.deb
RUN curl https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.70/linux64/chromedriver-linux64.zip -o /usr/src/chromedriver-linux64.zip && \
    unzip /usr/src/chromedriver-linux64.zip -d /usr/src && \
    cp /usr/src/chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver

# ABOVE are only required for challenge 1

RUN apt install -y nodejs npm python3 python3-pip gcc
RUN npm install -g webppl --registry=https://registry.npmmirror.com

COPY requirements.txt /root
RUN pip3 install --break-system-packages -r /root/requirements.txt

RUN echo 'fake{get flag1 on the real server}' > /flag1
RUN echo 'fake{get flag2 on the real server}' > /flag2

COPY driver.sh /root
COPY xssbot.py /root
COPY webppl_site.zip /root
RUN unzip -d /root /root/webppl_site.zip

WORKDIR /root
CMD ["/usr/bin/python3", "-u", "/root/xssbot.py"]
