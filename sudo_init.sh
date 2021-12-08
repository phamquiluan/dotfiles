#!/bin/sh

CUR_DIR="$(pwd)"

# Install necessary utilities
apt-get update -y && apt-get upgrade -y

# Clone vim and compile from souce
git clone https://github.com/vim/vim.git
cd vim/src
PY3_CONFIG=$(python3-config --configdir)
./configure --with-x 			    \
    --enable-multibyte                      \
    --enable-python3interp=dynamic          \
    --with-python3-config-dir=$PY3_CONFIG

make -j8
make install
cd ../..

# Copying config files
cp .bashrc ~/.bashrc
cp .bash_aliases ~/.bash_aliases
cp .vimrc ~/.vimrc
cp .ycm_extra_conf.py ~/.ycm_extra_conf
cp .inputrc ~/.inputrc
cp .tmux.conf ~/.tmux.conf

# Setup YouCompleteMe
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
vim +PluginInstall +qall
cd ~/.vim/bundle/YouCompleteMe
python3 install.py


# Install fzf
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
bash ~/.fzf/install --all


echo "DONE"
