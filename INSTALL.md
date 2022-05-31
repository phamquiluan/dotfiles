# dotfiles

An instruction to install a new Linux machine


### steps:

**Update and Upgrade**

```bash 
sudo apt-get update -y && sudo apt-get upgrade -y 
```

**Install nvidia drivers**

In the Additional Drivers section.

**Switch Capslock and Escape** 

```bash
gnome-tweaks

remember to chown -R user:user /home/user
```


**Install Python**
```bash
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa

# update source list to focal
sudo apt update -y

# install python
sudo apt-get install -y python3.6 python3.6-dev python3.6-venv
sudo apt-get install -y python3.7 python3.7-dev python3.7-venv
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
