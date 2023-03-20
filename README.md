# dotfiles

[![Linter](https://github.com/phamquiluan/dotfiles/actions/workflows/linter.yml/badge.svg?branch=master)](https://github.com/phamquiluan/dotfiles/actions/workflows/linter.yml)

The instruction to install a my Linux machine (tested on Debian, Ubuntu 20.04, 21.10, and 22.04). Use at your own risk!

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [The Landscape](#the-landscape)
- [Installation](#installation)
  - [(optional) customize partitions during OS installation](#optional-customize-partitions-during-os-installation)
  - [step-by-step](#step-by-step)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


# The Landscape

![image](https://user-images.githubusercontent.com/24642166/219843721-16a31616-27bc-4bcf-b267-f3e0b9765a55.png)

# Installation

## (optional) customize partitions during OS installation

https://askubuntu.com/questions/343268/how-to-use-manual-partitioning-during-installation

- /docker  # 100GB for /var/lib/docker
- /workspaces  # 100GB 
- /home/luan  # 160GB
- /  # the rest for os
- /data         (HDD, datasets, films)

note:
- using etcher to make bootable usb for debian https://github.com/balena-io/etcher
- [debian-live-11.6.0-amd64-gnome+nonfree.iso](https://cdimage.debian.org/cdimage/unofficial/non-free/cd-including-firmware/current-live/amd64/iso-hybrid/)

## step-by-step

<details>
<summary>Update and upgrade</summary>
  
```bash 
sudo apt-get update -y && sudo apt-get upgrade -y 
  
sudo apt-get install -y htop git curl unzip \
  libncurses5-dev libxt-dev libx11-dev libxtst-dev \
  libssl-dev libsqlite3-dev libreadline-dev \
  libtk8.6 libgdm-dev libdb4o-cil-dev libpcap-dev \
  build-essential cmake xclip software-properties-common \
  rsync tmux ripgrep
```
</details> 




<details>
<summary>Install Nvidia drivers</summary>

Check the Additional Drivers section.

or run the following commands
```bash
sudo apt-get install nvidia-drive.. <tab>
```
then, REBOOT
</details>
  
<details>
<summary>Switch Capslock and Escape</summary>

```bash
gnome-tweaks

remember to chown -R user:user /home/user
```
</details>





<details>
<summary>Install Python from 3.7 to 3.10</summary>  
  
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update -y

sudo apt-get install -y python3.7 python3.7-dev python3.7-venv
sudo apt-get install -y python3.8 python3.8-dev python3.8-venv
sudo apt-get install -y python3.9 python3.9-dev python3.9-venv
sudo apt-get install -y python3.10 python3.10-dev python3.10-venv

```
</details>




<details>
<summary>Compile Vim</summary>

Clone Vim. Read and follow the instruction carefully
```
git clone git@github.com:vim/vim.git
cd vim
cat src/INSTALL
```

Ensure vim is compile with clipboard and python3 support.
```bash
vim --version | grep clipboard
vim --version | grep python
```
</details>


<details>
<summary>Copy dotfiles and install Vim / YCM / Plugins</summary>
  
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

python3 install.py --verbose
```
or
```bash
python3 install.py --go-completer --rust-completer --ts-completer --verbose
```

Give a little care about JsCompleter, remove tern
https://github.com/ycm-core/YouCompleteMe#javascript-and-typescript-semantic-completion
</details>
  
 
 
 
<details> 
<summary>Install FZF</summary>

```bash
sudo apt install ripgrep
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
bash ~/.fzf/install --all
```
</details>




<details>
<summary>Install Docker / Docker Compose / Docker Nvidia</summary>

Install docker
```bash
curl https://get.docker.com | sh \
  && sudo systemctl --now enable docker
  
sudo usermod -aG docker $USER
```
Reboot! Test by `docker run hello-world` or `docker run ubuntu`

Change docker image storage location: https://www.ibm.com/docs/en/cloud-private/3.1.1?topic=pyci-specifying-default-docker-storage-directory-by-using-bind-mount

Install docker nvidia, https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

Install docker compose, https://docs.docker.com/compose/install/
</details>
  
  
  
  
  
<details>
<summary>Install common softwares</summary>
  
- Chrome
- Zoom
- Slack 
- Mendeley
- Ibus Bamboo
- Mendeley: https://www.mendeley.com/autoupdates/installers/1.19.8
- Zotero
- Team
- Telegram
  
```bash
wget https://github.com/phamquiluan/dotfiles/releases/download/v0.0.1/mendeleydesktop-1.19.8-linux-x86_64.tar.bz2
sudo mv mendeleydesktop-1.19.8-linux-x86_64.tar.bz2 /
sudo tar xvf mendeleydesktop-1.19.8-linux-x86_64.tar.bz2
cd mendeleydesktop-1.19.8-linux-x86_64
sudo ./bin/installer....
```

start by `m`
</details>




<details>
  <summary>Install AWSCLI</summary>

```bash
# https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```
</details>


<details>
  <summary>Install kubectl</summary>

```bash
sudo curl --silent --location -o /usr/local/bin/kubectl \
   https://amazon-eks.s3.us-west-2.amazonaws.com/1.19.6/2021-01-05/bin/linux/amd64/kubectl

sudo chmod +x /usr/local/bin/kubectl
```
</details>

<details>
  <summary>Install Helm</summary>

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```
</details>

<details>
<summary>Install Kind</summary>

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.17.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```
</details>
  
  
<details>
<summary>Install Minikube</summary>

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```
</details>
  
  
<details>
<summary>Install Skaffold</summary>

```bash
# For Linux x86_64 (amd64)
curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64 && \
sudo install skaffold /usr/local/bin/
```
</details>
  
<details>
<summary>Install GCloud CLI</summary>

https://cloud.google.com/sdk/docs/install#deb
</details>
  
  
  
# Candidate
  
- httpie
- postman
- my-weather-indicator
- ubuntu my weather indicator
- zotero
  
  
# note
- wifi adapter driver: https://deb.trendtechcn.com/
- if don't see wifi: check this 
  `sudo mv /usr/lib/firmware/iwlwifi-ty-a0-gf-a0.pnvm  /usr/lib/firmware/iwlwifi-ty-a0-gf-a0.bak` and reboot
                       https://askubuntu.com/questions/1360175/intel-wifi-6-ax210-wifi-not-working-after-update/1360291#1360291
- if boot time is too slow, use `sudo systemd-analyze blame/critical-chain` can help to detect the root cause.
- last time, i encountered this bug, the solution is to use `sudo systemctl mask <servicename>.service`
                       https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=959985
- minimize, maximize button: gsettings set org.gnome.desktop.wm.preferences button-layout ":minimize,maximize,close"
   https://askubuntu.com/questions/651347/how-to-bring-back-minimize-and-maximize-buttons-in-gnome-3              
- USB often auto disconnect (debian bug) https://www.kernel.org/doc/Documentation/usb/power-management.txt
   https://ywjheart.wordpress.com/2018/07/17/disable-usb-auto-suspend-in-ubuntu-debian/
