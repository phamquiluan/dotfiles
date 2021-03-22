#!/bin/sh

CUR_DIR="$(pwd)"

APT_CMD=$(which apt)

printf "\n===== Installing build-essential cmake vim.. ====="
if [ ! -z $APT_CMD ]; then 
	sudo apt update -y && sudo apt upgrade -y
	sudo add-apt-repository ppa:jonathonf/vim -y
	sudo apt update -y && sudo apt upgrade -y
	sudo apt install -y build-essential cmake

	# install vim 8.2
	sudo apt install -y vim
	
	# https://stackoverflow.com/questions/65284572/your-c-compiler-does-not-fully-support-c17
	sudo apt-get install g++-8
	sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 700 --slave /usr/bin/g++ g++ /usr/bin/g++-7
	sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 800 --slave /usr/bin/g++ g++ /usr/bin/g++-8
else
	printf "\nNOT SUPPORT :))"
	exit 1
fi

printf "\n===== Copying config files.. ====="
cp .bashrc ~/.bashrc
cp .bash_aliases ~/.bash_aliases
cp .vimrc ~/.vimrc
cp .ycm_extra_conf.py ~/.ycm_extra_conf
cp .inputrc ~/.inputrc
cp .tmux.conf ~/.tmux.conf

printf "\n===== Setup YouCompleteMe.. ====="
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
vim +PluginInstall +qall
cd ~/.vim/bundle/YouCompleteMe
python3 install.py


printf "\n===== Install fzf.. ====="
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
bash ~/.fzf/install --all


printf "\n==== DONE ===="
