#!/bin/sh

CUR_DIR="$(pwd)"

sudo apt-get update -y && sudo apt-get upgrade -y
echo "Install necessary utilities"
sudo apt-get install -y \
	python3-dev \
	git \
	libncurses5-dev \
	unzip \
	libxt-dev \
	libx11-dev \
	libxtst-dev \
	build-essential

git clone git@github.com:Kitware/CMake.git && cd CMake && ./bootstrap && make && sudo make install

echo "===== Clone vim and compile from souce ====="
git clone https://github.com/vim/vim.git
cd vim/src
PY3_CONFIG=$(python3-config --configdir)
./configure --with-x 			    \
    --enable-multibyte                      \
    --enable-python3interp=dynamic          \
    --with-python3-config-dir=$PY3_CONFIG

make -j8
sudo make install
cd ../..

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


sudo apt-get install g++-8
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 700 --slave /usr/bin/g++ g++ /usr/bin/g++-7
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 800 --slave /usr/bin/g++ g++ /usr/bin/g++-8

echo "===== Setup YouCompleteMe.. ====="
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
vim +PluginInstall +qall
cd ~/.vim/bundle/YouCompleteMe
python3 install.py


echo "===== Install fzf.. ====="
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
bash ~/.fzf/install --all


echo "==== DONE ===="
