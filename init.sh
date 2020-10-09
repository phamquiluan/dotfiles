#!/bin/sh

if [ ! -d "$HOME/anaconda3" ] || [ ! -d "$HOME/miniconda3" ] ;
then
	echo "Conda could not be found! Installing conda.."
	wget "https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.3-Linux-x86_64.sh"
	bash Miniconda3-py37_4.8.3-Linux-x86_64.sh -b -p "$HOME/miniconda3"
else
	echo "Conda is found!!!"
fi


CUR_DIR="$(pwd)"

YUM_CMD=$(which yum)
APT_CMD=$(which apt)

echo "===== Installing build-essential cmake vim.. ====="
if [ ! -z $APT_CMD ]; then 
	sudo add-apt-repository ppa:jonathonf/vim -y
	sudo apt update -y && sudo apt upgrade -y
	sudo apt install -y build-essential cmake vim-gtk
elif [ ! -z $YUM_CMD ]; then
	sudo yum update -y
	sudo yum install -y build-essential cmake vim-gtk
else
	echo "NOT SUPPORT"
	exit 1
fi

echo "===== Copying config files.. ====="
cp .bashrc ~/.bashrc
cp .bash_aliases ~/.bash_aliases
cp .vimrc ~/.vimrc
cp .ycm_extra_conf.py ~/.ycm_extra_conf
cp .inputrc ~/.inputrc
cp .tmux.conf ~/.tmux.conf

echo "===== Setup YouCompleteMe.. ====="
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
vim +PluginInstall +qall
cd ~/.vim/bundle/YouCompleteMe
python3 install.py --clang-completer


cd $CUR_DIR
echo "===== Copy vim template ====="
cp -r templates ~/.vim/templates


echo "===== Install fzf.. ====="
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
bash ~/.fzf/install --all


echo "==== DONE ===="
