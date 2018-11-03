É melhor usar o ubuntu com interface gráfica por conta dos drives: 

    apt-get install cups smbclient foomatic-gui foomatic-db


Em /etc/cups/cupsd.conf

Listen localhost:631
Listen 192.168.100.74:631

DefaultEncryption Never # testar

<Location />
  Allow from 192.168.100.0/24
  Order allow,deny
</Location>

<Location /admin>
  Allow from localhost
  Allow from 192.168.100.1
  Order allow,deny
</Location>

Acessar 192.168.100.74:631 no browser
e logar com o usuário root do servidor

restart cups

smb.conf
[printers]
    browseable = no
    path = /var/spool/samba/
    printable = yes
    guest ok = yes
    read only = yes
    create mask = 0700

