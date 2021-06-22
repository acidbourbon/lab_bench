
# the following uncommented lines are the Dockerfile contents of
# image acidbourbon/ubuntu_cernroot_python3
# we're gonna save ourselves the effort of compiling root by using a prebuilt container

# #---------------------------
# 
# ##################################################
# ##    intermediate stage to build CERN ROOT     ##
# ##################################################
# 
# 
# FROM ubuntu:18.04
# 
# USER root
# 
# ARG DEBIAN_FRONTEND=noninteractive
# 
# RUN apt-get update && \
#   apt-get -y install \
#   libgslcblas0 \
#   python3-numpy \
#   python3-scipy \
#   python3-matplotlib \
#   liblapack3 \
#   libboost-all-dev \
#   wget \
#   git dpkg-dev cmake g++ gcc binutils libx11-dev libxpm-dev \
#   libxft-dev libxext-dev
# 
# RUN wget https://root.cern/download/root_v6.18.02.source.tar.gz && tar -zxvf root_v6.18.02.source.tar.gz && rm root_v6.18.02.source.tar.gz
# 
# # arguments for cmake to use python3 for pyROOT
# RUN mkdir /root-build && cd /root-build; cmake -DPYTHON_EXECUTABLE=/usr/bin/python3 ../root-6.18.02
# 
# RUN cd /root-build; make -j6
# 
# ##################################################
# ##        build actual working container        ##
# ##################################################
# 
# # leave some 500 MB of root source files behind
# 
# FROM ubuntu:18.04
# 
# USER root
# 
# ARG DEBIAN_FRONTEND=noninteractive
# 
# RUN apt-get update && \
#   apt-get -y install \
#   vim \
#   nano \
#   libgslcblas0 \
#   python3-numpy \
#   python3-scipy \
#   python3-matplotlib \
#   bc \
#   liblapack3 \
#   libboost-all-dev 
# 
# 
# COPY --from=0 /root-build /root-build 
# 
# 

FROM acidbourbon/ubuntu_cernroot_python3:2019-09-29

USER root

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
  apt-get -y install \
  gv ghostscript xterm x11-utils \
  dialog \
  libgfortran3 \
  libgslcblas0 \
  wine-stable \
  iputils-ping \
  curl \
  perl \
  git \
  python3-pip \
  liblapack3 \
  libboost-all-dev \
  wget \
  tmux \
  emacs \
  imagemagick
  
  
RUN pip3 install --upgrade pip
RUN pip3 install setuptools && \
  pip3 install pythondialog python-vxi11 \
  jupyter \
  numpy scipy pyltspice python-vxi11 \
  pyserial \
  requests \
  jsonrpclib

# for garfield to feel at home make symlink to som gsl libs
RUN ln -s /usr/lib/x86_64-linux-gnu/libgslcblas.so.0.0.0 /usr/lib/libgsl.so.0 

# this will create /LTspiceXVII with all the 
# windows binaries and libraries you'll need
ADD ./build/LTspiceXVII.tgz /



# in case you need that win32 support some time ... seems not important
#RUN dpkg --add-architecture i386 && apt-get update && apt-get -y install wine32

RUN cd /opt; git clone https://github.com/lambdalisue/jupyter-vim-binding

ENV HOME=/workdir
RUN echo "#!/bin/bash\n. /root-build/bin/thisroot.sh; export PYTHONPATH=\$PYTHONPATH:/workdir/python_modules;\
 cd /workdir; ./start.sh " >entrypoint.sh ; chmod +x entrypoint.sh
ENTRYPOINT "/entrypoint.sh"




