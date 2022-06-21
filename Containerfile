FROM fedora:latest

# Install documentation for DNF packages
RUN sed -i 's/tsflags=nodocs//' /etc/dnf/dnf.conf
RUN echo "max_parallel_downloads=10" >> /etc/dnf/dnf.conf
RUN echo "fastestmirror=True" >> /etc/dnf/dnf.conf

# Full image update, and install development tools
RUN dnf -y update &&  dnf install -y cmake man-db man man-pages neovim tmux nodejs git bash-completion zsh clang-tools-extra @C\ Development\ Tools\ and\ Libraries python-pip

# Edit sudoers to allow wheel group to sudo without password
RUN sed -i 's/^%wheel/# %wheel/' /etc/sudoers && \
    echo '%wheel ALL=(ALL) NOPASSWD: ALL' | sudo EDITOR='tee -a' visudo

# Some default variables that can be changed at build time
ARG UNAME=dev
ARG UID=1000
ARG GID=1000

# Create the user, group, and project folder
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -G wheel -o -s /usr/bin/zsh $UNAME
RUN mkdir /project

# Change user and working dir to $UNAME
WORKDIR /home/$UNAME
USER $UNAME:$UNAME

# Setup nvim
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
RUN curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
RUN sed -i "s/plugins=(git)/plugins=(git tmux)/" ~/.zshrc
RUN sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="gnzh"/' ~/.zshrc

# Setup tmux
RUN git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
# tmux plugins
RUN echo "set -g @plugin 'tmux-plugins/tpm'" >> ~/.tmux.conf
RUN echo "set -g @plugin 'tmux-plugins/tmux-sensible'" >> ~/.tmux.conf

# end tmux plugins
# additional tmux configs
RUN echo run '~/.tmux/plugins/tpm/tpm' >> ~/.tmux.conf

# Add init.nvim
RUN mkdir -p ~/.conf/nvim/
COPY --chown=${UID}:${GID} init.vim /home/${UNAME}/.config/nvim/init.vim

# Install Plugins
RUN nvim --headless +PlugInstall +qa
RUN nvim --headless +'CocInstall -sync coc-yaml coc-sh coc-git coc-docker coc-clangd coc-json coc-pyright' +qa

# Change working dir to project directory
WORKDIR /project
