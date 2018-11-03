LTSP: 

Colocar o Internet na eth1 e a rede interna na eth0. 

1) Configurar uma das placas de redes para rede interna, neste exemplo eth0. 
Editar o arquivo: gedit /etc/network/interfaces
Colocar seguinte conteúdo:
auto eth0
iface eth0 inet static
    address 192.168.1.1
    netmask 255.255.255.0
    network 192.168.1.0
    broadcast 192.168.1.255

auto eth1
iface eth1 inet dhcp

2) Instalar pacote: apt-get install ltsp-server-standalone

3) gedit /etc/default/isc-dhcp-server e colocar a linha: 
INTERFACES="eth0"

4) gedit /etc/ltsp/dhcpd.conf
subnet 192.168.1.0 netmask 255.255.255.0 {
    range 192.168.1.20 192.168.1.100;
    option domain-name-servers 192.168.1.1;
    option broadcast-address 192.168.1.255;
    option router 192.168.1.1;
}

5)Criar imagem no LTSP, no terminal: 
ltsp-build-client --arch i386
ltsp-update-sshkeys

***Opcionais
6) se quiser criar diretórios compartilhados, criar em /etc/skel

7) rodar comando na imagem: 
chroot /opt/ltsp/i386 apt-get install vim
e depois atualizar: ltsp-update-image

8) Ver se o tftpd-hpa gerou um número de processo, em caso negativo, reinstalá-lo. 

9) extra:
firewall:
echo 1 > /proc/sys/net/ipv4/ip_foward
iptables -t nat -A POST ROUTING -o eth0 -j MASQUERADE

