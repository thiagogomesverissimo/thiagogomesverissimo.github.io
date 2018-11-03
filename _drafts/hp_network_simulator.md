# HNS - HP Network Simulator

Baixar o simulador: 

 - http://h20564.www2.hpe.com/hpsc/swd/public/readIndex?sp4ts.oid=7107838&swLangOid=8&swEnvOid=4062

A versão HNS 7.1.50 (última disponível para Linux) de 64 bits só funcionar no 
Ubuntu 14.04/trusty e não no Ubuntu 16.04/Xenial. A versão HNS 7.1.50 32 bits 
funciona em ambas versão do Ubuntu.


## Configurando acesso via SSH:

Carregue essa configuração no HNS depois de criar uma rede host-only no virtualbox:

    device_id = 1
    device_model = SIM1100
    board = SIM1101 : memory_size 1024
    # conferir com ifconfig se é vboxnet0, vboxnet1 ...
    device 1: interface 1 <--> host : "vboxnet2"

Depois de acessar a VM no Virtualbox:

    # Colocar ip na porta de manutenção:
    display interface brief
    system-view
    interface M-Ethernet 1/0/1
    ip address 192.168.100.15 24
    quit
    
    # Habilitando SSH:
    SSH server enable
    public-key local create rsa
    line vty 0 4 
    authentication-mode scheme
    protocol inbound ssh 
    quit
    local-user thiago
    password simple teste
    service-type ssh
    authorization-attribute user-role network-admin
    quit 
    save force
    display current-configuration


## Tutoriais bacanas

Vídeos demostrativos:

 - https://www.brainshark.com/HP-ESSN/vu?pi=zGlz14Ff6mzL7Caz0&r3f1=063c42111d595d5a4d066306555a4d050252067a5e1543001d180a54351900034c1c1051403b440e040d155a55453b52100e17015a565e3943090c171d070a5e3ad0e685cb95d4d7d38b&fb=1
