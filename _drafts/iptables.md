ver se está instalado: 
 dpkg -l | grep iptables

-mostra as regras existentes na lista: iptables -L FORWARD
-adiciona uma nova regra na FIM da lista de input: iptables -A INPUT
-adiciona uma nova regra na INICIO da lista de input: iptables -I INPUT 
-remove uma regra da lista de input: iptable -D INPUT
-remove a regra da lista INPUT número 2: iptables _D INPUT 2
-altera a politica padrão: iptables -P INPUT DROP
-remove todas as regras existentes: iptables -F ou iptables -F INPUT
-substitui a regra input 4: iptables -R INPUT 4 "nova regra"
-Insere uma nova chain chamada thiago na tabela filter: iptables -t filter -N thiago
-renomeia a chain thiago para thais: iptables -E thiago thais
-apaga a chain thais: iptables -X thais

Esquema geral:
 iptables [-t tabela] -[comando] [situação (chain)] especificação-da-regra [alvo]
 -A INPUT -i eth0: adcionar regra no fim da lista input 
 -A OUTPUT -o eth0: adicionar regra no fim da lista output
 -j: alvo do pacote: DROP (ou REJECT: avisa ao emissor do pacote), ACCEPT, REDIRECT(para mudar a porta --to-port)
 -p: protocolo, neste caso tcp
 -s: origem do pacote
 -d: destino da pacote
 --dport: porta de destino do pacote
 --sport: porta de destino

Exemplo:
 iptables  
  -t filter 
  -A INPUT 
  -i eth0 
  -s 192.168.1.1/24 
  -d 192.168.1.2/24 
  -p tcp 
  --sport 45222 
  --dport 6881 
  -j ACCEPT


  -Neste exemplo, pacotes de respostas de ICMP serão aceitos somente se recebidos em um intervalo de tempo de 1 segundo ( -m limit --limit 1/s -j ACCEPT ). Caso algum pacote ultrapasse este limite imposto pela regra, esta deverá automaticamente executar a regra seguinte:
    iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s -j ACCEPT

  -Esta regra irá bloquear qualquer pacote ICMP que chegar:
    iptables -A INPUT -p icmp -j DROP

  -Qualquer nova conexão que parta da interface eth0 seja rejeitada:
    iptables -A INPUT -m state --state NEW -i eth0 -j DROP

  -Bloqua qualquer pacote proveniente deste dispositivo de rede cujo endereço mac foi referenciado.
    iptables -A INPUT -m mac --mac-source 00:0F:B0:C2:0C:5C -j DROP

  -Bloqueia todos os pacotes vindo de ppp0 para as portas 21 (ftp), 23 (telnet), 25 (smtp), 80 (www), 110 (pop3), 113 (ident), 6667 (irc). 
    iptables -A INPUT -p tcp -i ppp0 -m multiport --destination-port 21,23,25,80,110,113,6667 -j DROP

  -Bloqueia qualquer tentativa de acesso ao programa Kazaa(usando o módulo -m string):
    iptables -A INPUT -m string --string "X-Kazaa" -j DROP

  -Não permite que dados confidenciais sejam enviados para fora da empresa e registra o ocorrido:
    iptables -A OUTPUT -m string --string "conta" -j LOG --log-prefix "ALERTA: dados confidencial "
    iptables -A OUTPUT -m string --string "conta" -j DROP

  -Somente permite a passagem de pacotes que não contém ".exe" em seu conteúdo (! diferente de):
    iptables -A INPUT -m string --string ! ".exe" -j ACCEPT

  -Rejeita conexões indo para portas UDP de pacotes criados pelo usuários pertencentes ao grupo 100. 
    iptables -A OUTPUT -m owner --gid-owner 100 -p udp -j DROP

NAT:
  -Antes de utilizar regra que utilize NAT: echo "1" > /proc/sys/net/ipv4/ip_forward
  -Sempre que fizermos um SNAT utilizaremos a situação (chain) POSTROUTING 
  -Sempre que fizermos um DNAT utilizaremos a situação (chain) PREROUTING.

Exemplos:
  -Todos os pacotes que saírem pela eth0 terão os endereços de origem alterados para 192.168.1.223:
    iptables -t nat -A POSTROUTING -o eth0 -j SNAT --to 192.168.1.233

  -Pacotes que chegam na interface eth0 terão o destino alterado para 192.168.1.233 
    iptables -t nat -A PREROUTING -i eth0 -j DNAT --to 192.168.1.233

  -Para fazermos redirecionemtos num mesmo host usamos proxy transparente usando redirect (não confidir com DNAT que muda o host), neste exemplo os pacotes que chegam pela porta 80 na interface eth0 são redirecionados para porta 3128
    iptables -t nat PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 3128 

  -compartilhar a internet: 
  -Neste exemplo, todos os IP's da rede 192.168.1.0 com máscara de rede 255.255.255.0 serão "mascarados". 
    iptables -t nat -A POSTROUTING -o lo -d 127.0.0.0/8 -j ACCEPT 
    iptables -t nat -A POSTROUTING DROP
    iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o eth0 -j MASQUERADE 

TOS (tipo de serviço do pacote), podemos configurar prioridades:
  -Aplicar a todos pacotes saindo por eth0, porta de destino 3306 e protocolo tcp a prioridade mínima (16)   
    iptables -t mangle -A OUTPUT -o eth0 -p tcp --dport 3306 -j TOS --set-tos 16

  -Prioridade de espera mínima aos pacotes que chegam por eth0 com porta de origem entre 6666 e 6668.
    iptables -t mangle -A PREROUTING -i eth0 -p tcp --sport 6666-6668 -j TOS --set-tos 0x10

  -priorizar todo o tráfego de IRC de nossa rede interna indo para a interface ppp0: 
    iptables -t mangle -A OUTPUT -o ppp0 -p tcp --dport 6666-6668 -j TOS --set-tos 16 

  -priorizar a transmissão de dados ftp saindo da rede: 
    iptables -t mangle -A OUTPUT -o ppp0 -p tcp --dport 20 -j TOS --set-tos 8 

  -Confere prioridade máxima à todos os pacotes que saem por eth0 com porta de destino 21:
    iptables -t mangle -A OUTPUT -o eth0 --dport 21 -j TOS --set-tos 16 

Exemplo de uma implementação:
-------------------------------------------
#!/bin/sh

start() {
  iptables -A INPUT -i lo -j ACCEPT 
  iptables -A INPUT -p tcp  --dport 80 -j ACCEPT 
  iptables -A INPUT -p tcp -s 143.107.8.10 --dport 5432  -j ACCEPT 

  #ignorar pings 
  iptables -A INPUT -p icmp --icmp-type echo-request -j DROP

  #protege contra pacotes malformados 
  iptables -A INPUT -m state --state INVALID -j DROP

  #proteje contra IP spoofing
  echo 1 > /proc/sys/net/ipv4/conf/default/rp_filter

  # Acessar via ssh
  iptables -A INPUT -p tcp --dport 45222 -j ACCEPT 

  #Bloquear todas conexões vindas de fora
  iptables -A INPUT -p tcp --syn -j DROP

  echo "Regras de Firewall ativadas"
}

stop(){
  iptables -F
  iptables -P INPUT ACCEPT
  iptables -P PUTPUT ACCEPT
  echo "Regras desativadas -  Perigo!!!"
} 

case "$1" in
    "start") start ;;
    "stop") stop ;;
    "restart") stop; start ;;
    *) echo "Use parametros start ou stop";
esac 