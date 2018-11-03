
Registrar domínios:
 -http://br.godaddy.com
 -http://www.enom.com/

Bind
 -apt-get install dnsutils
 -apt-get install bind9

nslookup
 -A porta usada no nslookup usa porta 53
 -ponto significa: a partir da raiz procure com.br 
 -$ nslookup
  >server 198.41.0.4
  >set q=any
  >br.
  >server  200.160.0.10

#Criando uma zona: 
 **VEr o que é a zona /etc/bind/zones.rfc1918?????????
 -No master: editar arquivo: /etc/bind/named.conf.local
 -adicionar no arquivo: (Colocar IP do DNS secundário em allow-transfer):
   zone "local.dev" 
     {
       type master;
       file "/etc/bind/db.dev";
       allow-transfer {193.169.0.11}; 
     };
 -allow-transfer: especifica quem assume caso o master caia

 -No Slave (secundário)
   zone "local.dev" 
     {
       type slave;
       file "/etc/bind/db.dev";
       masters {193.169.0.10; };
     };

 -Em /etc/hosts do master e secundário:
   193.169.0.10 dnsprimario.local.dev dnsprimario
   193.169.0.11 dnssecundario.local.dev dnssecundario

 -No master: criar arquivo /etc/bind/db.dev (há um modelo: /etc/bind/db.empty):
   -dnsprimario é o hostname da máquina
   -thiago.local.dev significa thiago@local.dev, o e-mail do admnistrador
   -SOA: start of authority
   -3H 15M 1W 1D: 
    -3H: o secundário atualiza a cada 3 horas, e se o master não responde assume
    -15M: tempo para o secundário assumir a zona (transferência de zona) de 15 em 15 minutos
    -1W: tempo máximo que o secundário assumirá a zona (para arrumar o master).
    -1D: tempo mínimo para que o secundário devolverá a zona para o master, caso o master volte para o ar.
   -NS: name server, server responsáveis pelo domínio (pode ter mais que uma linha)
   -MX: Mail Exchange, servidor de e-mail (pode ter mais que uma linha: prioridades: 10,20...)
   -Se existir, cadastrar o dns secundário na lista de subdomínios: dnssencudario A 193.169.0.11
   -A/IN CNAME: A: Address mappring e IN CNAME: apelido (em ipv6 usar AAAA ao invés de A) 
------------------------------------------------------------------------------------------------
      @       IN      SOA     dnsprimario.local.dev. thiago.local.dev. (2014060801 3H 15M 1W 1D )
      NS      dnsprimario.local.dev.
      NS      dnssecundario.local.dev.
      IN      MX      10      mail.local.dev.
      IN      MX      20      mailreserva.local.dev.
      local.dev.      A       193.169.0.10
      www     A       193.169.0.10
      ftp     A       193.169.0.15
      dnssecundario     A       193.169.0.11
      sites	IN CNAME ftp 
      uol IN CNAME www.uol.com.br. ;exemplo de CNAME externo
------------------------------------------------------------------------------------------------
 -logs do bind: tail -f -n 30 /var/log/syslog | grep named 
 -Perguntar para o DNS primario quem é: www.local.dev
   $ dig www.local.dev @193.169.0.10


#Criando uma zona: 
 **VEr o que é a zona /etc/bind/zones.rfc1918?????????
 -No master: editar arquivo: /etc/bind/named.conf.local
 -adicionar no arquivo: (Colocar IP do DNS secundário em allow-transfer):
   zone "local.dev" 
     {
       type master;
       file "/etc/bind/db.dev";
       allow-transfer {193.169.0.11}; 
     };
 -allow-transfer: especifica quem assume caso o master caia

 -No Slave (secundário)
   zone "local.dev" 
     {
       type slave;
       file "/etc/bind/db.dev";
       masters {193.169.0.10; };
     };

 -Em /etc/hosts do master e secundário:
   193.169.0.10 dnsprimario.local.dev dnsprimario
   193.169.0.11 dnssecundario.local.dev dnssecundario

 -No master: criar arquivo /etc/bind/db.dev (há um modelo: /etc/bind/db.empty):
   -dnsprimario é o hostname da máquina
   -thiago.local.dev significa thiago@local.dev, o e-mail do admnistrador
   -SOA: start of authority
   -3H 15M 1W 1D: 
    -3H: o secundário atualiza a cada 3 horas, e se o master não responde assume
    -15M: tempo para o secundário assumir a zona (transferência de zona) de 15 em 15 minutos
    -1W: tempo máximo que o secundário assumirá a zona (para arrumar o master).
    -1D: tempo mínimo para que o secundário devolverá a zona para o master, caso o master volte para o ar.
   -NS: name server, server responsáveis pelo domínio (pode ter mais que uma linha)
   -MX: Mail Exchange, servidor de e-mail (pode ter mais que uma linha: prioridades: 10,20...)
   -Se existir, cadastrar o dns secundário na lista de subdomínios: dnssencudario A 193.169.0.11
   -A/IN CNAME: A: Address mappring e IN CNAME: apelido (em ipv6 usar AAAA ao invés de A) 
------------------------------------------------------------------------------------------------
      @       IN      SOA     dnsprimario.local.dev. thiago.local.dev. (2014060801 3H 15M 1W 1D )
      NS      dnsprimario.local.dev.
      NS      dnssecundario.local.dev.
      IN      MX      10      mail.local.dev.
      IN      MX      20      mailreserva.local.dev.
      local.dev.      A       193.169.0.10
      www     A       193.169.0.10
      ftp     A       193.169.0.15
      dnssecundario     A       193.169.0.11
      sites	IN CNAME ftp 
      uol IN CNAME www.uol.com.br. ;exemplo de CNAME externo
------------------------------------------------------------------------------------------------
 -logs do bind: tail -f -n 30 /var/log/syslog | grep named 
 -Perguntar para o DNS primario quem é: www.local.dev
   $ dig www.local.dev @193.169.0.10


secundario

Registrar domínios:
 -http://br.godaddy.com
 -http://www.enom.com/

Bind
 -apt-get install dnsutils
 -apt-get install bind9

nslookup
 -A porta usada no nslookup usa porta 53
 -ponto significa: a partir da raiz procure com.br 
 -$ nslookup
  >server 198.41.0.4
  >set q=any
  >br.
  >server  200.160.0.10

#Criando uma zona: 
 **VEr o que é a zona /etc/bind/zones.rfc1918?????????
 -No master: editar arquivo: /etc/bind/named.conf.local
 -adicionar no arquivo: (Colocar IP do DNS secundário em allow-transfer):
   zone "local.dev" 
     {
       type master;
       file "/etc/bind/db.dev";
       allow-transfer {193.169.0.11}; 
     };
 -allow-transfer: especifica quem assume caso o master caia

 -No Slave (secundário)
   zone "local.dev" 
     {
       type slave;
       file "/etc/bind/db.dev";
       masters {193.169.0.10; };
     };

 -Em /etc/hosts do master e secundário:
   193.169.0.10 dnsprimario.local.dev dnsprimario
   193.169.0.11 dnssecundario.local.dev dnssecundario

 -No master: criar arquivo /etc/bind/db.dev (há um modelo: /etc/bind/db.empty):
   -dnsprimario é o hostname da máquina
   -thiago.local.dev significa thiago@local.dev, o e-mail do admnistrador
   -SOA: start of authority
   -3H 15M 1W 1D: 
    -3H: o secundário atualiza a cada 3 horas, e se o master não responde assume
    -15M: tempo para o secundário assumir a zona (transferência de zona) de 15 em 15 minutos
    -1W: tempo máximo que o secundário assumirá a zona (para arrumar o master).
    -1D: tempo mínimo para que o secundário devolverá a zona para o master, caso o master volte para o ar.
   -NS: name server, server responsáveis pelo domínio (pode ter mais que uma linha)
   -MX: Mail Exchange, servidor de e-mail (pode ter mais que uma linha: prioridades: 10,20...)
   -Se existir, cadastrar o dns secundário na lista de subdomínios: dnssencudario A 193.169.0.11
   -A/IN CNAME: A: Address mappring e IN CNAME: apelido (em ipv6 usar AAAA ao invés de A) 
------------------------------------------------------------------------------------------------
      @       IN      SOA     dnsprimario.local.dev. thiago.local.dev. (2014060801 3H 15M 1W 1D )
      NS      dnsprimario.local.dev.
      NS      dnssecundario.local.dev.
      IN      MX      10      mail.local.dev.
      IN      MX      20      mailreserva.local.dev.
      local.dev.      A       193.169.0.10
      www     A       193.169.0.10
      ftp     A       193.169.0.15
      dnssecundario     A       193.169.0.11
      sites	IN CNAME ftp 
      uol IN CNAME www.uol.com.br. ;exemplo de CNAME externo
------------------------------------------------------------------------------------------------
 -logs do bind: tail -f -n 30 /var/log/syslog | grep named 
 -Perguntar para o DNS primario quem é: www.local.dev
   $ dig www.local.dev @193.169.0.10
