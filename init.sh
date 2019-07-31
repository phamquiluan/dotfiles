#!/bin/sh

cp bashrc ~/.bashrc
cp vimrc ~/.vimrc
cp ycm_extra_conf.py ~/.ycm_extra_conf

git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
vim +PluginInstall +qall
cd ~/.vim/bundle/YouCompleteMe
python3 install.py

input='requirements.txt'
while IFS= read -r line
do
	pip install "$line"
done < "$input"
