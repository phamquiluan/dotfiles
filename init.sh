#!/bin/sh

if [ ! $CONDA_DEFAULT_ENV ];
then
	wget 'https://repo.continuum.io/archive/Anaconda3-5.3.1-Linux-x86_64.sh'
	bash Anaconda3-5.3.1-Linux-x86_64.sh
fi


cur_dir="$(pwd)"

sudo apt install build-essential cmake vim

echo "Copying source files..."
cp .bashrc ~/.bashrc
cp .bash_aliases ~/.bash_aliases
cp .vimrc ~/.vimrc
cp .ycm_extra_conf.py ~/.ycm_extra_conf

echo "Setup Vim, YouCompleteMe"
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
vim +PluginInstall +qall
cd ~/.vim/bundle/YouCompleteMe
python3 install.py --clang-completer


cd $cur_dir
echo "copy vim template"
cp -r templates ~/.vim/templates


echo "Install fzf"
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
bash ~/.fzf/install


echo "==== DONE ===="
