FROM fedora:latest

# Install documentation for DNF packages
RUN sed -i 's/tsflags=nodocs//' /etc/dnf/dnf.conf

# Full image update, and install findutils (find & xargs) and wget
RUN dnf -y update &&  dnf install -y man-db man man-pages vim tmux nodejs git bash-completion clang-tools-extra @C\ Development\ Tools\ and\ Libraries

# Edit sudoers to allow wheel group to sudo without password
RUN sed -i 's/^%wheel/# %wheel/' /etc/sudoers && \
    echo '%wheel ALL=(ALL) NOPASSWD: ALL' | sudo EDITOR='tee -a' visudo

# Some default variables that can be changed at build time
ARG UNAME=dev
ARG UID=1000
ARG GID=1000

# Create the user, group, and project folder
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -G wheel -o -s /bin/bash $UNAME
RUN mkdir /project


# Change user and working dir to $UNAME
WORKDIR /home/$UNAME
USER $UNAME:$UNAME
ENV PS1="<<dev>>[\u@\h \W] "

# Add the .vimrc
COPY --chown=$UID:$GID vimrc .vimrc
COPY --chown=$UID:$GID gdbinit .gdbinit

# Install Coc.nvim
RUN mkdir -p /home/$UNAME/.vim/pack/coc/start
RUN mkdir -p /home/$UNAME/.vim/pack/themes/start

COPY --chown=$UID:$GID coc.nvim /home/$UNAME/.vim/pack/coc/start/coc.nvim
COPY --chown=$UID:$GID dracula /home/$UNAME/.vim/pack/themes/start/dracula

# Install coc-plugins
RUN cd /home/$UNAME/.vim/pack/coc/start && \
    vim -c "helptags coc.nvim/doc/|q" && \
    vim -c 'CocInstall -sync coc-yaml coc-sh coc-git coc-docker coc-clangd coc-json coc-pyright|q|q'

# Change working dir to project directory
WORKDIR /project
