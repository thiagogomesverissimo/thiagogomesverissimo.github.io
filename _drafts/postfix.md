Boas práticas
 -É importante ter o hostname definido no arquivo /etc/hosts para que o Postfix de forma geral funcione satisfatoriamente
  127.0.0.1 localhost.localdomain localhost
  192.168.1.12 example.org example

-Certifique-se de que o "nome curto" do servidor (example) seja o único conteúdo do arquivo /etc/hostname 
  hostname -f
  hostname

-Verifique também se existe uma entrada de nameserver apontando para seu próprio IP (pode ser o loopback também) no arquivo 
  /etc/resolv.conf
  search example.org

Verificar o postfix
  dnsdomainname
  postconf
  postconf -e mydomain="`dnsdomainname`"
  postconf mydomain
