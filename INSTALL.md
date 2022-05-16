# dotfiles

An instruction to install a new Linux machine


### steps:

**Update and Upgrade**

```bash 
sudo apt-get update -y && sudo apt-get upgrade -y 
```

**Install nvidia drivers**

In the Additional Drivers section.

**Install Python**
```bash
sudo apt-get install python3.9 python3.9-venv python3.9-dev
```

**Copy dotfiles and install Vim / YCM / Plugins**
```bash
cp .bashrc ~/.bashrc
cp .bash_aliases ~/.bash_aliases
cp .vimrc ~/.vimrc
cp .ycm_extra_conf.py ~/.ycm_extra_conf
cp .inputrc ~/.inputrc
cp .tmux.conf ~/.tmux.conf

git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
vim +PluginInstall +qall
cd ~/.vim/bundle/YouCompleteMe
python3 install.py --all
```


**Install FZF**

```bash
if [ -n -d "~/.fzf" ]; then
    git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
fi
bash ~/.fzf/install --all
```

**Install Docker / Docker Compose / Docker Nvidia**

Install docker
```bash
# install docker
curl https://get.docker.com | sh \
  && sudo systemctl --now enable docker
  
# test by `docker run hello-world` or `docker run ubuntu`
```

Install docker nvidia, https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

Install docker compose, https://docs.docker.com/compose/install/

**Install common softwares**

- Chrome
- Zoom
- Slack 
- Mendeley
- Ibus Bamboo
