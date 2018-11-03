coloca no boot:  
 update-rc.d apache2 defaults 

expirar contar:
 
usermod -e "September 20, 2014"

remove do boot: 
 update-rc.d apache2 defaults 

compactar1: 
 tar -vzcf file.tar.gz /home/thiago
 tar -vzjf file.tar.gz /home/thiago

descompactar bzip2: 
 tar -vjxf file.tar.bz2

programar reboot: 
 shutdown -r +6:00

Link: 
 ln -s /var/www/site meu_link

## Fazer usuário a trocar senha no próximo login:
  
    chage -d 0

## Fazer o usuário trocar de senha a cada 60 dias:

    chage -M 60 bianca

Novo usuário com home:
 adduser thiago
 deluser thiago --remove-home

ou
  userdel -r thiago

Grupo: 
 addgroup todos
 delgroup todos

Add usuário no grupo todos: 
 adduser usuario todos

Pegar UUID: 
 blkid /dev/sda1

reparando partição: 
 fsck.ext4 /dev/sda1

montar: 
 mount -t ext4 /dev/sda2 /mnt/thiago

remontar a seco:
 mount -o remount rw /particao

suporte ntfs mkfs: 
  sudo apt-get install ntfs-3g

suporte vfat mkfs: 
  sudo apt-get install dosfstools


Criando patições:
  fdisk /dev/sda 

Formatar e XFS: 
  aptitude install xfsprogs
  mkfs.xfs -f /dev/sdb1

Módulos habilitados:
  lsmod

Identificações dos dispositivos físicos conectador:
  lsusb
  lspci 

Módulos adicionais no kernel:
  modprobe teste #carrega no módulo "teste" no kernel
  modprobe -r teste # descarrega módulo teste
  modprobe #lista módulos disponíveis

Processo:
  cat /proc/net/dev
  cat /proc/cpuinfo 

Lista tamahos de arquivos:
  du -h 
  du -sh

Permissões:
  4: leitura
  2: Edição
  1: execução

Listagem ordenada por tamanho:
  ls -lS

Gravar cd:
  wodim --help

Move o output para null:
  ls &>/dev/null

Rede
  /etc/network/interfaces
   auto eth0
   iface eth0 inet static
    address 172.16.6.8
    netmask 255.255.248.0
    network 172.16.0.0
    broadcast 172.16.7.255
    gateway 172.16.0.1
   auto eth0:1
   iface eth0:1 inet static
    address 172.16.6.9
    netmask 255.255.248.0
    network 172.16.0.0
    broadcast 172.16.7.255
    gateway 172.16.0.1
   dns-nameservers 127.0.0.1 143.107.8.20 143.107.253.3 143.107.253.5

#Colocar no cron:
 23 07 02 * * * ntpdate -s ntp.usp.br
 24 14 04 * * * aptitude update && aptitude upgrade -y




find . -type f -exec sed -i "s/Desktop\/mygits/repos/g" {} \;

#eval "$(ssh-agent -s)"
#ssh-add
hostnamectl set-hostname sti-035374

# Instalando java: 

    dpkg-query -l | grep openjdk
    sudo apt-get remove --purge openjdk-7-jre* 
    sudo apt-get remove --purge openjdk-6-jre* 
    sudo apt-get autoremove
    sudo add-apt-repository ppa:webupd8team/java
    sudo apt-get update
    sudo apt-get install oracle-java8-installer

# adobe flash:

sudo add-apt-repository ppa:nilarimogard/webupd8
sudo apt-get update
sudo apt-get install browser-plugin-freshplayer-pepperflash

teclado ubuntu 14.04
setxkbmap -model abnt2 -layout br