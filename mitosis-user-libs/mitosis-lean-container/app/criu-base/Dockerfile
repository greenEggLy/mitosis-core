FROM ubuntu:16.04
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

RUN sed -i s/archive.ubuntu.com/mirror.sjtu.edu.cn/g /etc/apt/sources.list && \
    sed -i s/security.ubuntu.com/mirror.sjtu.edu.cn/g /etc/apt/sources.list

RUN chmod 777 /tmp

RUN apt update && apt install -y libcap-dev libnl-3-dev libnet1-dev pkg-config libbsd-dev flex bison libprotobuf-dev libprotobuf-c-dev protobuf-c-compiler protobuf-compiler python-protobuf build-essential git libmount-dev bc ffmpeg asciidoc

RUN rm -rf /var/lib/apt/lists/*

# TODO: to gitee src
#RUN GIT_SSL_NO_VERIFY=1 git clone --branch no_error_for_restore https://github.com/xiehongrui/criu.git
#WORKDIR /opt
#RUN --mount=type=bind,source=/root/mitosis/criu,target=/opt/criu

COPY criu /criu

RUN cd /criu && rm images/google/protobuf/descriptor.proto && ln -s /usr/include/google/protobuf/descriptor.proto images/google/protobuf/descriptor.proto && make -j $(nproc) && make install

RUN apt update && apt install -y python3 wget  python3-pip && rm -rf /var/lib/apt/lists/*
#&& wget https://bootstrap.pypa.io/pip/3.5/get-pip.py && python3 get-pip.py && rm -rf /var/lib/apt/lists/*

#RUN apt update && apt install -y criu

#RUN apt update && apt install -y bc ffmpeg && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .

# RUN pip install --progress-bar off -r requirements.txt -i https://mirror.sjtu.edu.cn/pypi/web/simple

#RUN mkdir -p /home/ly/
# RUN export PATH="/home/ly/miniconda3/bin:$PATH"
COPY Miniconda3-py310_23.1.0-1-Linux-x86_64.sh /root/Miniconda3-latest-Linux-x86_64.sh
RUN cd /root && sh Miniconda3-latest-Linux-x86_64.sh -b -p /root/miniconda3
#RUN /root/miniconda3/bin/pip install numpy pandas pyarrow moviepy -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN /root/miniconda3/bin/conda config --add channels https://mirror.sjtu.edu.cn/anaconda/pkgs/free \
	&& /root/miniconda3/bin/conda config --add channels https://mirror.sjtu.edu.cn/anaconda/pkgs/main \
	&& /root/miniconda3/bin/conda config --add channels https://mirror.sjtu.edu.cn/anaconda/pkgs/mro \
	&& /root/miniconda3/bin/conda config --add channels https://mirror.sjtu.edu.cn/anaconda/pkgs/msys2 \
	&& /root/miniconda3/bin/conda config --set show_channel_urls yes
#RUN /root/miniconda3/bin/conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main \
 #&& /root/miniconda3/bin/conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free \
 #&& /root/miniconda3/bin/conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r \
 #&& /root/miniconda3/bin/conda config --set show_channel_urls yes
RUN /root/miniconda3/bin/conda install -y numpy pandas pyarrow 
RUN /root/miniconda3/bin/conda install -y opencv orjson imageio
#RUN /home/ly/miniconda3/bin/pip install moviepy -i https://pypi.tuna.tsinghua.edu.cn/simple
#RUN pip3 install numpy pandas pyarrow moviepy -i https://pypi.tuna.tsinghua.edu.cn/simple
#RUN /home/ly/miniconda3/bin/pip install moviepy -i https://pypi.tuna.tsinghua.edu.cn/simple

#RUN chmod 775 /root/miniconda3/bin/python3.12 && chmod 775 /root/miniconda3/lib/python3.12/lib-dynload/*.so && chmod 775 /root/miniconda3/lib/*.so* && find /root/miniconda3/lib/python3.12/site-packages -type f -name "*.so*" -exec chmod 775 {} + 
#RUN chmod 664 /root/miniconda3/lib/libgcc_s.so.1
