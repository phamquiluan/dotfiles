#!/bin/sh

CUR_DIR="$(pwd)"

APT_CMD=$(which apt)

echo "Install necessary utilities"
sudo apt-get install -y \
	git \
	unzip \
	libxt-dev \
	build-essential \
	cmake

echo "===== Clone vim and compile from souce ====="
git clone https://github.com/vim/vim/archive/master.zip
unzip master.zip
cd vim-master
./configure --with-x
make -j8
sudo make install

# # https://stackoverflow.com/questions/65284572/your-c-compiler-does-not-fully-support-c17
# sudo apt-get install g++-8
# sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 700 --slave /usr/bin/g++ g++ /usr/bin/g++-7
# sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 800 --slave /usr/bin/g++ g++ /usr/bin/g++-8


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
python3 install.py


echo "===== Install fzf.. ====="
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
bash ~/.fzf/install --all


echo "==== DONE ===="
