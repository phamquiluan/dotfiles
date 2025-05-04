FROM ubuntu:latest

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies
RUN apt-get update -y && \
    apt-get install -y \
    htop git curl wget unzip \
    libncurses5-dev libxt-dev libx11-dev libxtst-dev \
    libssl-dev libsqlite3-dev libreadline-dev \
    libtk8.6 libgdm-dev libpcap-dev \
    build-essential cmake xclip software-properties-common \
    rsync tmux ripgrep gnome-tweaks clang libtool-bin \
    libpython3-dev python3-pip tldr zip poppler-utils tree jq man-db

# Install Python versions (3.8, 3.10, 3.12)
RUN add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update -y && \
    apt-get install -y \
    python3.8 python3.8-dev python3.8-venv \
    python3.10 python3.10-dev python3.10-venv \
    python3.12 python3.12-dev python3.12-venv

# Unminize for man pages
RUN yes | unminimize

# Clone and compile Vim with Python support
RUN git clone https://github.com/vim/vim.git /tmp/vim && \
    cd /tmp/vim && \
    ./configure --prefix=/usr/local --with-features=huge --enable-python3interp=yes && \
    make -j8 && \
    make install

# Verify Vim compilation
RUN vim --version | grep clipboard && \
    vim --version | grep python

# Install FZF
RUN git clone --depth 1 https://github.com/junegunn/fzf.git $HOME/.fzf && \
    $HOME/.fzf/install --all

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# Clone dotfiles repository
RUN git clone https://github.com/phamquiluan/dotfiles.git $HOME/dotfiles

# Copy dotfiles to the home directory
RUN cp $HOME/dotfiles/.bashrc $HOME/.bashrc && \
    cp $HOME/dotfiles/.bash_aliases $HOME/.bash_aliases && \
    cp $HOME/dotfiles/.vimrc $HOME/.vimrc && \
    cp $HOME/dotfiles/.ycm_extra_conf.py $HOME/.ycm_extra_conf.py && \
    cp $HOME/dotfiles/.inputrc $HOME/.inputrc && \
    cp $HOME/dotfiles/.tmux.conf $HOME/.tmux.conf

# Install Vundle and Vim plugins
RUN git clone https://github.com/VundleVim/Vundle.vim.git $HOME/.vim/bundle/Vundle.vim && \
    vim +PluginInstall +qall

# Install YouCompleteMe with all completers
RUN cd $HOME/.vim/bundle/YouCompleteMe && \
    python3 install.py --verbose --force-sudo

# Install Vim Copilot
RUN curl -fsSL https://deb.nodesource.com/setup_23.x -o nodesource_setup.sh && \
	bash nodesource_setup.sh && \
	apt-get install -y nodejs
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash
RUN git clone https://github.com/github/copilot.vim.git \
  ~/.vim/pack/github/start/copilot.vim


# Set the default shell to bash
ENV SHELL=/bin/bash
RUN git config --global user.email "phamquiluan@gmail.com" && \
	  git config --global user.name "Luan Pham" && \
	  git config --global alias.ci commit 

RUN mkdir -p /root/.local/share

# Set the working directory
WORKDIR /ws

# Start a shell session
CMD ["bash"]
