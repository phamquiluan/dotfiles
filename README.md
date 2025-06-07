# dotfiles

[![Build and Publish Docker image](https://github.com/phamquiluan/dotfiles/actions/workflows/docker-build-and-push.yml/badge.svg)](https://github.com/phamquiluan/dotfiles/actions/workflows/docker-build-and-push.yml)
[![Linter](https://github.com/phamquiluan/dotfiles/actions/workflows/linter.yml/badge.svg?branch=master)](https://github.com/phamquiluan/dotfiles/actions/workflows/linter.yml)

The instruction to install a my Linux machine (tested on Debian, Ubuntu 20.04, 21.10, and 22.04). Use at your own risk!

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [The Landscape](#the-landscape)
- [Installation](#installation)
  - [(optional) customize partitions during OS installation](#optional-customize-partitions-during-os-installation)
  - [step-by-step](#step-by-step)
- [Candidate](#candidate)
- [note](#note)
- [Macbook note](#macbook-note)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


# The Landscape

![image](https://user-images.githubusercontent.com/24642166/219843721-16a31616-27bc-4bcf-b267-f3e0b9765a55.png)

# Installation

Use [Etcher](https://github.com/balena-io/etcher) to make your USB stick

## (optional) customize partitions during OS installation

https://askubuntu.com/questions/343268/how-to-use-manual-partitioning-during-installation

- /docker  # 100GB for /var/lib/docker
- /workspaces  # 100GB 
- /home/luan  # 160GB
- /  # the rest for os
- /data         (HDD, datasets, films)

ISO download url:
- [debian-live-11.6.0-amd64-gnome+nonfree.iso](https://cdimage.debian.org/cdimage/unofficial/non-free/cd-including-firmware/current-live/amd64/iso-hybrid/)

## step-by-step

<details>
<summary>Update and upgrade</summary>
  
```bash 
sudo apt-get update -y 
  
sudo apt-get install -y htop git curl unzip \
  libncurses5-dev libxt-dev libx11-dev libxtst-dev \
  libssl-dev libsqlite3-dev libreadline-dev \
  libtk8.6 libgdm-dev libdb4o-cil-dev libpcap-dev \
  build-essential cmake xclip software-properties-common \
  rsync tmux ripgrep gnome-tweaks clang libtool-bin \
  libpython3-dev
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
<summary>Install Python from 3.8 to 3.12</summary>
  
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update -y

sudo apt-get install -y python3.8 python3.8-dev python3.8-venv
sudo apt-get install -y python3.10 python3.10-dev python3.10-venv
sudo apt-get install -y python3.12 python3.12-dev python3.12-venv
```
</details>




<details>
<summary>Compile Vim</summary>

Clone Vim. Read and follow the instruction carefully
```
git clone https://github.com/vim/vim.git
cd vim
cat src/INSTALL

./configure --prefix=$HOME/.local
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
<summary>Install Ripgrep</summary>

```bash
curl -LO 'https://github.com/BurntSushi/ripgrep/releases/download/14.1.0/ripgrep-14.1.0-x86_64-unknown-linux-musl.tar.gz'
tar xvf ripgrep-14.1.0-x86_64-unknown-linux-musl.tar.gz
cd ripgrep-14.1.0-x86_64-unknown-linux-musl
cp rg $HOME/.local/bin
chmod +x $HOME/.local/bin/rg
```
</details>
 

<details> 
<summary>Install tree without sudo</summary>

```bash
cd $HOME/.local/bin/
apt download tree
dpkg-deb -xv ./*deb ./
cp ./usr/bin/tree .
chmod +x tree
```
</details>
 
 
<details> 
<summary>Install FZF</summary>

```bash
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

https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html

```bash
sudo curl --location -o /usr/local/bin/kubectl \
   https://s3.us-west-2.amazonaws.com/amazon-eks/1.26.2/2023-03-17/bin/linux/amd64/kubectl

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
  <summary>Install Helmfile</summary>

- `helm plugin install https://github.com/databus23/helm-diff`
- Download the amd linux version from https://github.com/helmfile/helmfile/releases
- `curl -L -o helmfile_1.0.0-rc.5_linux_amd64.tar.gz https://github.com/helmfile/helmfile/releases/download/v1.0.0-rc.5/helmfile_1.0.0-rc.5_linux_amd64.tar.gz`
- untar, `sudo mv helmfile /usr/local/bin/`
- `sudo chmod +x /usr/local/bin/helmfile`

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
  
<details>
<summary>Install eksctl</summary>

https://github.com/eksctl-io/eksctl/blob/main/README.md#installation
</details>
  
<details>
<summary>Install k9s</summary>

  ```
     curl -sS https://webinstall.dev/k9s | bash
  ```
  https://github.com/derailed/k9s
</details>  
  
<details>
<summary>Install Vim Copilot</summary>

  - https://github.com/nodesource/distributions
  - https://github.com/nvm-sh/nvm  
  - https://github.com/github/copilot.vim
</details>  
  
  
# Candidate
  
- my-weather-indicator
- ubuntu my weather indicator
- zotero
- https://github.com/Valloric/dotfiles
- https://github.com/mzur/gnome-shell-wsmatrix
- https://istio.io/latest/docs/ops/diagnostic-tools/istioctl/
- https://github.com/vladimirvivien/ktop  
- https://github.com/BambooEngine/ibus-bamboo

  
# note
- In MacOS, up arrow and Ctrl + up arrow send the same signal: https://superuser.com/questions/660013/resizing-pane-is-not-working-for-tmux-on-mac
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
- ubuntu goes to grub command line everytime i boot: need to check wth is going on :)
  + boot repair doesn't help 
  + sudo ls /boot/efi/EFI/ -> it turns out `Debian` was there
  + sudo rm /boot/efi/EFI/Debian -> fixed it!!!
- etcher doesn't start? 
  ```bash
  /usr/bin/balena-etcher-electron --disable-gpu-sandbox   
  ```
- random app doesn't start?
  + locate it by `locate`, install by `mlocate`, inspect the `.desktop` file can be helpful
  + start it from terminal, hopefully you can catch something 
  ```bash 
  (ins)luan@kitty:~$ /opt/extras.ubuntu.com/my-weather-indicator/bin/my-weather-indicator
  Namespace GeocodeGlib not available
  Repository version required not present
  (ins)luan@kitty:~$ sudo apt-get install libgeocode-glib-dev
  [sudo] password for luan: 
  ```
- sudo apt list --upgradable / sudo apt install --only-upgrade code


# Macbook note

https://github.com/pyenv/pyenv?tab=readme-ov-file#macos

vi-mode in python  https://docs.python.org/3/library/readline.html

```
# file ~/.editrc
python:bind -v
python:bind ^I rl_complete
```
in .bashrc, need to have `export SHELL="/bin/bash"`, because tmux will look for this env var to create the shell, default is /bin/zsh

make the key repeat faster: https://apple.stackexchange.com/questions/10467/how-to-increase-keyboard-key-repeat-rate-on-os-x

tmux alt 2: https://superuser.com/questions/649960/option-key-does-not-work-as-meta-in-tmux

you can develop with Linux within Mac using docker
```
docker pull phamquiluan/dev:latest
docker tag phamquiluan/dev:latest dev:latest
docker run --platform linux/amd64 -v $HOME/ws:/ws -it dev:latest
```  

[tmux on macOS - copy to system clipboard](https://www.jdeen.com/blog/tmux-on-macos-copy-to-system-clipboard)
