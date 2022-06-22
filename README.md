# lab bench

## what is it?

This git contains scripts and a Dockerfile to generate a container which provides
a jupyter notebooks server and all sorts of python libs and examples for accessing
all sorts of lab equipment

## how to install it

clone this git and then procure all the submodules (other gits) that are
used in the container.

```
git clone https://github.com/acidbourbon/lab_bench
cd lab_bench
git submodule init
git submodule update
```
## how to update

update this git and all submodules (other gits) that are
used in the container.

```
git pull 
git submodule init
git submodule update
```

## how to build and start the container

make sure you have docker installed and your user is part of the "docker" group

```
sudo apt-get install docker.io
sudo usermod -a -G docker $USER
sudo reboot
```

start docker daemon
```
sudo service docker start
```

start the container

```
cd /path/to/lab_bench
./build_and_run.sh
```


point your web browser to the following address:
http://localhost:8888

look at the example notebooks

## LTspice

when you start the docker for the first time,
you have to start ~/ltspice.sh once for the stupid web sync thing
to show you its pop-up window. Only THEN you can run it successfully
in batch mode from python.

have fun with the software

## adding a git submodule
```
git submodule add https://github.com/acidbourbon/M8195A_scripts workdir/python_modules/M8195A_scripts
git submodule init
git submodule update

git commit -a -m "blah"
```
## updating a git submodule from within lab_bench
```
# you find yourself in a detached head unnamed branch of your submodule
git checkout main # or "master"
git commit -a -m "changes to submodule"
git push

cd .. # you are now in the lab_bench git

git commit -a -m "changes (including submodule changes) of lab_bench"
git push

```
