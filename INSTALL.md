# dotfiles
An instruction to install a new Linux machine (tested on Debian, and Ubuntu 21.10)

### customize partitions during installation

https://askubuntu.com/questions/343268/how-to-use-manual-partitioning-during-installation

- /root (40GB)
- /home/user (e.g. /home/luan)
- /docker 
- /data (HDD)


### steps:
<details>
<summary>Update and upgrade</summary>
  
```bash 
sudo apt-get update -y && sudo apt-get upgrade -y 
  
sudo apt-get install -y htop git curl unzip \
  libncurses5-dev libxt-dev libx11-dev libxtst-dev \
  libssl-dev libsqlite3-dev libreadline-dev \
  libtk8.6 libgdm-dev libdb4o-cil-dev libpcap-dev \
  build-essential cmake xclip mono-complete golang \
  nodejs default-jdk npm software-properties-common
```
</details> 





<details>
<summary>Install Nvidia drivers</summary>

Check the Additional Drivers section.
</details>
  
<details>
<summary>Switch Capslock and Escape</summary>

```bash
gnome-tweaks

remember to chown -R user:user /home/user
```
</details>





<details>
<summary>Install Python3.6 & Python3.7</summary>  
  
```bash
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa

# update source list to focal
sudo apt update -y

# install python
sudo apt-get install -y python3.6 python3.6-dev python3.6-venv
sudo apt-get install -y python3.7 python3.7-dev python3.7-venv
```
</details>





<details>
<summary>Compile Python3.8</summary>
  
```bash
curl -O https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tar.xz 
tar xvf Python-3.8.12.tar.xz
cd Python-3.8.12.tar.xz

./configure \
    LDFLAGS="-Wl,-rpath /usr/local/lib" \
    --enable-shared \
    --enable-optimizations \
    --enable-loadable-sqlite-extensions \
    --disable-ipv6 \
    --enable-big-digits=30 \
    --with-ensurepip="upgrade" \
    --with-lto \
    --with-assertions \
    --with-system-ffi
make -j10
sudo make install 
```
</details>





<details>
<summary>Compile Python3.9</summary>
  
```bash
curl -O https://www.python.org/ftp/python/3.9.13/Python-3.9.13.tar.xz 
tar xvf Python-3.9.13.tar.xz
cd Python-3.9.13.tar.xz

./configure \
        --enable-shared \
        --enable-optimizations \
        --enable-loadable-sqlite-extensions \
        --disable-ipv6 \
        --enable-big-digits=30 \
        --with-ensurepip="upgrade" \
        --with-lto \
        --with-assertions \
        --with-system-ffi
make -j10
sudo make install 
```
</details>





<details>
<summary>Compile Vim</summary>

```
git clone git@github.com:vim/vim.git
cd vim/vim

# read
cat src/INSTALL

# ensure vim is compile with clipboard and python3 support 
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
python3 install.py --go-completer --rust-completer --ts-completer --verbose
```

Give a little care about JsCompleter, remove tern
https://github.com/ycm-core/YouCompleteMe#javascript-and-typescript-semantic-completion
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
# install docker
curl https://get.docker.com | sh \
  && sudo systemctl --now enable docker
  
# test by `docker run hello-world` or `docker run ubuntu`
```

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
