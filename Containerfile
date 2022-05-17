FROM fedora:latest

ARG USERNAME="dev"
RUN groupadd ${USERNAME}
RUN useradd -m -g users -G wheel -s /bin/bash ${USERNAME}

RUN dnf -y update && dnf install -y vim tmux nodejs git man-db bash-completion findutils clang-tools-extra @C\ Development\ Tools\ and\ Libraries
RUN sed -i 's/^%wheel/# %wheel/' /etc/sudoers && \
    echo '%wheel ALL=(ALL) NOPASSWD: ALL' | sudo EDITOR='tee -a' visudo

WORKDIR /home/${USERNAME}
USER ${USERNAME}:users

COPY vimrc .vimrc
COPY installs installs
COPY ide.sh ide.sh

RUN mkdir -p /home/${USERNAME}/project
WORKDIR /home/${USERNAME}/project

RUN mkdir -p /home/${USERNAME}/.vim/pack/coc/start && \
    cd /home/${USERNAME}/.vim/pack/coc/start && \
    git clone --branch release https://github.com/neoclide/coc.nvim.git --depth=1

RUN mkdir -p ~/.vim/pack/themes/start && \
    cd ~/.vim/pack/themes/start && \
    git clone https://github.com/dracula/vim.git dracula && \
    cd /home/${USERNAME}/.vim/pack/coc/start && \
    vim -c "helptags coc.nvim/doc/ | q"

RUN mkdir -p ~/.config/tmux && \
    git clone https://github.com/tmux-plugins/tmux-sensible ~/config/tmux && \
    echo "run-shell ~/config/tmux/sensible.tmux" | sudo tee .tmux.conf

RUN sudo chmod +x ~/ide.sh

ENTRYPOINT ../ide.sh
