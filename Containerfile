FROM fedora:latest

# Install documentation for DNF packages
RUN sed -i 's/tsflags=nodocs//' /etc/dnf/dnf.conf

# Full image update, and install findutils (find & xargs) and wget
RUN dnf -y update &&  dnf install -y findutils wget

# Edit sudoers to allow wheel group to sudo without password
RUN sed -i 's/^%wheel/# %wheel/' /etc/sudoers && \
    echo '%wheel ALL=(ALL) NOPASSWD: ALL' | sudo EDITOR='tee -a' visudo

# Some default variables that can be changed at build time
ARG UNAME=tmp
ARG UID=1000
ARG GID=1000

# Create the user and group
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -G wheel -o -s /bin/bash $UNAME

# Change user and working dir to $UNAME
WORKDIR /home/$UNAME
USER $UNAME:$UNAME

# Add the .vimrc and the packages to be installed
COPY --chown=$UID:$GID vimrc .vimrc
COPY --chown=$UID:$GID installs installs

# Install items in installs
RUN sudo xargs -a installs -I {} dnf -y install {}

# Install Coc.nvim
RUN mkdir -p /home/$UNAME/.vim/pack/coc/start && \
    cd /home/$UNAME/.vim/pack/coc/start && \
    git clone --branch release https://github.com/neoclide/coc.nvim.git --depth=1

# Install vim theme & commonly used coc-plugins
RUN mkdir -p ~/.vim/pack/themes/start && \
    cd ~/.vim/pack/themes/start && \
    git clone https://github.com/dracula/vim.git dracula && \
    cd /home/$UNAME/.vim/pack/coc/start && \
    vim -c "helptags coc.nvim/doc/|q" && \
    vim -c 'CocInstall -sync coc-yaml|q|q' && \
    vim -c 'CocInstall -sync coc-sh|q|q' && \
    vim -c 'CocInstall -sync coc-git|q|q' && \
    vim -c 'CocInstall -sync coc-docker|q|q' && \
    vim -c 'CocInstall -sync coc-clangd|q|q' && \
    vim -c 'CocInstall -sync coc-json|q|q' && \
    vim -c 'CocInstall -sync coc-pyright|q|q'

# Install sensible tmux defaults and gdb-dashboard
RUN mkdir -p ~/.config/tmux && \
    git clone https://github.com/tmux-plugins/tmux-sensible ~/.config/tmux && \
    echo "run-shell ~/config/tmux/sensible.tmux" | tee .tmux.conf && \
    wget -P ~ https://git.io/.gdbinit && \
    mkdir -p ~/project

# Change working dir to project directory
WORKDIR /home/$UNAME/project
