
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

RUN apt-get update && \
  apt-get -y install \
  texlive-xetex texlive-fonts-recommended texlive-latex-recommended

RUN apt-get update && \
  apt-get -y install \
  python3-sympy \
  python3-pandas

RUN apt-get update && \
  apt-get -y install \
  libdevice-serialport-perl \
  gnuplot

#
#RUN apt-get update && \
#  apt-get -y install \
#  libcairo2-dev libpango1.0-dev ffmpeg
#
#RUN pip3 install --upgrade pip
#RUN pip3 install setuptools && \
#  pip3 install pythondialog python-vxi11 \
#  jupyter \
#  numpy scipy pyltspice python-vxi11 \
#  pyserial \
#  requests \
#  jsonrpclib
#RUN pip3 install manim

RUN apt-get update && \
  apt-get -y install \
  libgslcblas0 \
  python3-numpy \
  python3-scipy \
  python3-matplotlib \
  liblapack3 \
  libboost-all-dev \
  wget \
  git dpkg-dev cmake g++ gcc binutils libx11-dev libxpm-dev \
  libxft-dev libxext-dev


# ##################################################
# ##      trying to build Go4 into lab_bench      ##
# ##################################################


RUN apt-get update && \
  apt-get -y install \
  subversion \
  qt5-qmake \
  libhdf5-dev \
  cmake \
  qt5-default



RUN mkdir -p /installations/go4; \
cd /installations/go4; \
# enable this to get most recent developer version
#svn co https://subversion.gsi.de/go4/trunk 601-00/
#enable this for tag 6.2.0
svn co https://subversion.gsi.de/go4/tags/602-00 602-00/

# we change default to build against hdf5 libs here:
#COPY build/Makefile.discover /installations/go4/602-00/build/


# crude hack
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN . /root-build/bin/thisroot.sh; \
    cd /installations/go4/602-00; \
    make -j6 withweb=1
#RUN echo "Installation of Go4 6.2.0 done!"
#RUN mv /root/.vnc/xstartup /root.vnc/xstartup.old 
#COPY conf/xstartup_lxqt /root/.vnc/xstartup

RUN echo ". /root-build/bin/thisroot.sh; export PYTHONPATH=\$PYTHONPATH:/workdir/python_modules; export PATH=\$PATH:/installations/go4/602-00/bin;  cd /workdir; ./start.sh " >entrypoint.sh ; chmod +x entrypoint.sh
ENTRYPOINT "/entrypoint.sh"






# Set the locale - fixes some problems with voila on the command line
RUN apt-get -y install locales
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8 

RUN pip3 install --upgrade pip
RUN pip3 install voila
