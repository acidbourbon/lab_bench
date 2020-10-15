#!/bin/bash

mkdir -p $(jupyter --data-dir)/nbextensions
cp /opt/jupyter-vim-binding $(jupyter --data-dir)/nbextensions/vim_binding -R

if [ -e /workdir/jupyter/enable_vim_binding ]; then
  jupyter nbextension enable vim_binding/vim_binding
else
  jupyter nbextension disable vim_binding/vim_binding
fi

jupyter notebook --port 8888 --no-browser --ip 0.0.0.0 --NotebookApp.token=''
