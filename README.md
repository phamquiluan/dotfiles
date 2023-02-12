# dotfiles
An instruction to install a new Linux machine for a Computer Science folk (tested on Debian, Ubuntu 20.04, 21.10, and 22.04)

![image](https://user-images.githubusercontent.com/24642166/218310302-2cbf0d11-37dc-4492-b483-3d4c4fc24656.png)

### (optional) customize partitions during OS installation

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
  build-essential cmake xclip software-properties-common
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

# update source list to focal
sudo apt update -y

# install python
sudo apt-get install -y python3.7 python3.7-dev python3.7-venv
sudo apt-get install -y python3.8 python3.8-dev python3.8-venv
sudo apt-get install -y python3.9 python3.9-dev python3.9-venv
sudo apt-get install -y python3.10 python3.10-dev python3.10-venv

```
</details>




<details>
<summary>Compile Vim</summary>

```
git clone git@github.com:vim/vim.git
cd vim

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

python3 install.py --verbose

# or
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
# install docker
curl https://get.docker.com | sh \
  && sudo systemctl --now enable docker
  
# add user to docker group
sudo usermod -aG docker $USER

# reboot
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
- Mendeley: https://www.mendeley.com/autoupdates/installers/1.19.8
  
```bash
wget https://github.com/phamquiluan/dotfiles/releases/download/v0.0.1/mendeleydesktop-1.19.8-linux-x86_64.tar.bz2
sudo mv mendeleydesktop-1.19.8-linux-x86_64.tar.bz2 /
sudo tar xvf mendeleydesktop-1.19.8-linux-x86_64.tar.bz2
cd mendeleydesktop-1.19.8-linux-x86_64
sudo ./bin/installer....
  
# start by
m 
```
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
# for completion
echo 'source <(kubectl completion bash)' >> ~/.bashrc 
echo 'alias k=kubectl' >> ~/.bashrc 
echo 'complete -o default -F __start_kubectl k' >> ~/.bashrc
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
