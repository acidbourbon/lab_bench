#!/bin/bash

xhost +si:localuser:$USER    
xhost +si:localuser:root  

name=$(basename $(pwd))

docker build -t $name . || exit

docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix \
--name $name -v $(pwd)/workdir:/workdir \
-p 8888:8888 \
-v /dev:/dev \
--privileged \
--rm -it --user $(id -u) $name 


#--device /dev/ttyACM0:/dev/ttyACM0 \
