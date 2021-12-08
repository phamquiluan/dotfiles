#!/bin/sh

CUR_DIR="$(pwd)"

# Install necessary utilities
apt-get update -y && apt-get upgrade -y && apt-get install -y libssl-dev


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
head -n 190 .vimrc > ~/.vimrc
cp .ycm_extra_conf.py ~/.ycm_extra_conf
cp .inputrc ~/.inputrc
cp .tmux.conf ~/.tmux.conf

# Setup YouCompleteMe
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
vim +PluginInstall +qall
cd ~/.vim/bundle/YouCompleteMe

git clone https://github.com/Kitware/CMake.git && cd CMake && ./bootstrap && make && make install && cd ..

apt-get install -y g++-8
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 700 --slave /usr/bin/g++ g++ /usr/bin/g++-7
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 800 --slave /usr/bin/g++ g++ /usr/bin/g++-8

python3 install.py


curl -LO https://github.com/BurntSushi/ripgrep/releases/download/13.0.0/ripgrep_13.0.0_amd64.deb
dpkg -i ripgrep_13.0.0_amd64.deb

# Install fzf
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
bash ~/.fzf/install --all


echo "DONE"
