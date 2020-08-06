---
title: 'Tópicos em proxmox'
date: 2020-04-10
permalink: /posts/proxmox
categories:
  - tutorial
tags:
  - proxmox
---

Anotações sobre proxmox.

<ul id="toc"></ul>

## Nested Virtualization com Debian e virt-manager

É muito útil ter um proxmox local para aplicar configurações
de testes antes de enviá-las para produção. 
Eu normalmente subo o proxmox usando o virt-manager habilitando
a opção nested virtualization.

{% highlight bash %}
    sudo apt install virt-manager
{% endhighlight %}

Para nested virtualization, há dois casos. Se seu processador for AMD:
{% highlight bash %}
    sudo su
    echo "options kvm-amd nested=1" > /etc/modprobe.d/kvm-amd.conf
    modprobe -r kvm_amd
    modprobe kvm_amd
{% endhighlight %}

E se for intel:
{% highlight bash %}
    sudo su
    echo "options kvm-intel nested=Y" > /etc/modprobe.d/kvm-intel.conf
    modprobe -r kvm_intel
    modprobe kvm_intel
{% endhighlight %}

Agora é só fazer o download da ISO do proxmox e iniciar a instalação do pelo
virt-manager:

 - https://www.proxmox.com/en/downloads/category/iso-images-pve

O diretório padrão do libvirt para salvar as VMs é
`/var/lib/libvirt/images/`, se quiser mudar, faça o procedimento abaixo:

{% highlight bash %}
sudo su
mkdir /home/storage_libvirt
chown libvirt-qemu: /home/storage_libvirt/

virsh pool-destroy default
virsh pool-undefine default
virsh pool-define-as --name default --type dir --target /home/storage_libvirt
virsh pool-autostart default
virsh pool-start default
{% endhighlight %}

Dicas gerais do proxmox:

- Baixando templates para containers: Datacenter->node->local(storage)->Content->Templates
- Subindo imagens ISO: Datacenter->node->local(storage)->Content->Upload

## NAT com Debain para as VMs

Existe inumeras formas de você criar um NAT, sendo uma das mais famosas, 
com o uso do pfsense. Aqui farei de forma bem simples, usando um container
do proxmox com debian, que vou chamar de `gw`.

Adicione uma segunda interface em no seu node: node->Network->Create->Linux Bridge. 
Se você colocar no campo *Bridge Port* alguma placa física, essa interface terá 
comunicação com sua rede local, fora do proxmox. Minha placa bridge ficou com o nome 
*vmbr1*. 

O container *gw* já está com acesso a rede externa na interface eth0 em bridge com *vmbr0*,
assim, vou apenas fazer a configuração de *vmbr1*. Para tal, eu desliguei o container 
(por algum motivo não consegui adicionar a interface com o container ligado). 
Em *container-gw->Network->Add* criei uma interface chamada *eth1* e selecionei bridge para *vmbr1*.

Criarei uma rede NAT  10.0.0.0/24. Depois de ligar o container tenha certeza 
que o comando *ip a* mostre tanto a
eth0, interface com saida para web, quanto eth1.

Em */etc/network/interfaces* colocaremos a configuração da nova interface:

{% highlight bash %}
auto eth1
iface eth1 inet static
        address  10.0.0.1
        netmask  255.255.255.0
        bridge_ports none
        bridge_stp off
        bridge_fd 0
        post-up echo 1 > /proc/sys/net/ipv4/ip_forward
        post-up   iptables -t nat -A POSTROUTING -s '10.0.0.0/24' -o eth0 -j MASQUERADE
        post-down iptables -t nat -D POSTROUTING -s '10.0.0.0/24' -o eth0 -j MASQUERADE
{% endhighlight %}

Agora suba a interface com `ifup eth1` e está feito.

## DHCP

## Encaminhamento de portas
