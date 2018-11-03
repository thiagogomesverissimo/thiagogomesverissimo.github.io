# Instalação:
 
    apt-get install virtualbox
    apt-get install virtualbox-guest-additions-iso
    apt-get install vagrant

# Sites para baixar box:

 - http://cloud-images.ubuntu.com/vagrant/
 - http://www.vagrantbox.es/
 - https://atlas.hashicorp.com/boxes/search

# Baixando box para ubuntu:
    
    url=http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-i386-vagrant-disk1.box
    vagrant box add thiago_trusty32 $url

# Baixando box para debian:

    url=https://pety.dynu.net/cloudbank_repo/debian_jessie_32bit.box
    vagrant box add debian-jessie32 $url --insecure

# Removendo box:

    vagrant box remove thiago_trusty32

# See available boxes in system:
  
    vagrant box list
    ls ~/.vagrant.d/boxes/

# Installing GUEST adds on VM

    vagrant plugin install vagrant-vbguest

# Generate Vagrantfile:

    mkdir meuprojeto
    cd meuprojeto
    vagrant init thiago_trusty32 # Cria o arquivo Vagrantfile
    vagrant up
    vagrant ssh

# Shutdown or suspend a VM:

    vagrant halt 
    vagrant halt --force
    vagrant suspend 

#Delete a VM:

    cd meuprojeto
    vagrant destroy

#Vagrantfile
  config.vm.box = "precise64"
  config.vm.box_url = 'http://files.vagrantup.com/precise64.box'
  #config.vm.box = "trusty64"
  #config.vm.box_url = 'http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box'
  config.vm.network :forwarded_port, guest: 80, host: 8080
  config.vm.synced_folder "/home/thiago/local", "/var/www"
  config.vm.network :private_network, ip: "193.169.0.5"
  config.vm.hostname = "my.dev"

  #Some Configuration of VM
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "512"]
  end

  #puppet
  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "manifests"
    puppet.manifest_file  = "base.pp"
  end

#Create my box
  $ vagrant halt
  $ vagrant package
  $ vagrant box add name_of_box arquivo.box

#Fix problem with GUEST additions Virtualbox
  1)vagrant plugin install vagrant-vbguest
  2)vagrant ssh -c 'sudo ln -s /opt/VBoxGuestAdditions-4.3.10/lib/VBoxGuestAdditions /usr/lib/VBoxGuestAdditions'
  3)vagrant reload
