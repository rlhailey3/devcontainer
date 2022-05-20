#!/bin/bash
git clone --branch release https://github.com/neoclide/coc.nvim.git --depth=1
git clone https://github.com/dracula/vim.git dracula
wget https://git.io/.gdbinit -O gdbinit
wget https://raw.githubusercontent.com/rlhailey3/devcontainer/main/vimrc -O vimrc
