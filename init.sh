#!/bin/sh

wget 'https://repo.continuum.io/archive/Anaconda3-5.3.1-Linux-x86_64.sh'
bash Anaconda3-5.3.1-Linux-x86_64.sh

cur_dir="$(pwd)"
echo "Copying source files..."
cp bashrc ~/.bashrc
cp vimrc ~/.vimrc
cp ycm_extra_conf.py ~/.ycm_extra_conf

echo "Setup Vim, YouCompleteMe"
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
vim +PluginInstall +qall
cd ~/.vim/bundle/YouCompleteMe
python3 install.py --clang-completer

cd $cur_dir
input='requirements.txt'
while IFS= read -r line
do
	pip install "$line"
done < "$input"
echo "********************************"
echo " 	       oɹǝɥ ʎw sı ǝǝʇ		  "
echo "********************************"
