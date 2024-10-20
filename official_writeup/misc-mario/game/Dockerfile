FROM node:20-bookworm

RUN apt update && apt install -y \
    git python3 python3-tk python3-pil python3-pil.imagetk \
    build-essential cmake libsdl2-dev qt6-base-dev \
    libminizip-dev zlib1g-dev libgl1-mesa-dev \
    supervisor x11vnc xterm xvfb novnc openbox \
    libnss3 libasound2 libatk-adaptor libgtk-3-0 libgbm1

WORKDIR /root
RUN git clone https://github.com/TASEmulators/fceux.git

ENV DISPLAY=:0.0 \
    DISPLAY_WIDTH=512 \
    DISPLAY_HEIGHT=448

COPY fceux-v2.6.6-patch.diff /root
RUN cd /root/fceux && git checkout v2.6.6 && git apply /root/fceux-v2.6.6-patch.diff --whitespace=fix && \
    mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release -DQT6=1 .. && make -j

COPY judger /root/judger
COPY launcher /root/launcher

RUN cd /root/launcher/ui && npm install --registry=https://registry.npmmirror.com

COPY vnc_lite.html /usr/share/novnc

ENTRYPOINT [ "/bin/bash" ]
CMD ["/root/launcher/entrypoint.sh"]
