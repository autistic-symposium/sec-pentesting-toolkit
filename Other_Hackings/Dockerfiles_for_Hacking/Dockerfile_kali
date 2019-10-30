FROM officialkali/kali
MAINTAINER steev@kali.org

RUN echo "deb http://http.kali.org/kali sana main contrib non-free" > /etc/apt/sources.list && \
echo "deb-src http://http.kali.org/kali sana main contrib non-free" >> /etc/apt/sources.list && \
echo "deb http://security.kali.org/kali-security sana/updates main contrib non-free" >> /etc/apt/sources.list && \
echo "deb-src http://security.kali.org/kali-security sana/updates main contrib non-free" >> /etc/apt/sources.list
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update && apt-get -y dist-upgrade && apt-get clean

CMD ["/bin/bash"]

