#!/bin/sh

CUR_DIR="$(pwd)"

sudo apt-get update -y && sudo apt-get upgrade -y
echo "Install necessary utilities"
sudo apt-get install -y \
	htop \
	python3-dev \
	git \
	libncurses5-dev \
	unzip \
	libxt-dev \
	libx11-dev \
	libxtst-dev \
	build-essential \
	cmake \
	vim-nox \
	xclip \
	g++-8
	mono-complete \
	golang \
	nodejs \
	default-jdk \
	npm

echo "===== Copying config files.. ====="
cp .bashrc ~/.bashrc
cp .bash_aliases ~/.bash_aliases
cp .vimrc ~/.vimrc
cp .ycm_extra_conf.py ~/.ycm_extra_conf
cp .inputrc ~/.inputrc
cp .tmux.conf ~/.tmux.conf

echo "===== Copying SSH config file.. ====="
if [ -n -d $HOME/.ssh ]; then
	mkdir $HOME/.ssh
fi
cp .ssh/config $HOME/.ssh/config


echo "===== Setup YouCompleteMe.. ====="
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
vim +PluginInstall +qall
cd ~/.vim/bundle/YouCompleteMe
python3 install.py --all


echo "===== Install fzf.. ====="
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
bash ~/.fzf/install --all


echo "==== DONE ===="
