# Modelo VirtualHost, criar /etc/apache2/sites-available/dev.conf:

    <VirtualHost *:80>
      ServerAdmin thiago@dev.local
      DocumentRoot /home/dev
      ServerName dev.local
      ServerAlias dev.local www.dev.local
      RewriteEngine On
      RewriteOptions inherit
              ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

      <Directory /home/dev>
        Options All
        Allowoverride All
      </Directory>
    </VirtualHost>

# Hanilita módulo:

    a2enmod rewrite
    a2ensite dev.conf 
    service apache2 reload

#Redirecionamento via htaccess

<IfModule mod_rewrite.c> !opcional o if
Options +FollowSymLinks
     RewriteEngine on
     RewriteRule (.*) http://revistas.usp.br/literartes/$1 [R=301,L]
</IfModule>

# Tunning

 - Na instalação padrão do apache2, o módulo prefork é o default.
   StartServers         30
   MinSpareServers      20
   MaxSpareServers      40
   MaxClients           310
   MaxRequestsPerChild  900

 -Valores Ideais
  -StartServers: Um pouco maiores que o número médio de conexões. 
  -MinSpareServer: Número mínimo de processos que ficarão esperando por requisições.
  -MaxSpareServer: Número máximo de processos que ficarão esperando por requisições.
  -MaxRequestChild: Número de requisições que responde até encerrar o processo,
    deve ser grande para responder pelas conexões no mesmo processo, sem abrir vários processos. 
  -MaxClient: Fazer o seguinte cálculo:
   -Média de consumo por processo:
   -ps -ylC apache2 --sort:rss
   -Na oitava coluna (RSS) vemos a média que cada processo do apache consome da RAM. 
   -Ver a memória consuminda pelo SO sem o apache rodando, pegar 80% da memória disponível. 
   -Dividir a memória acima pela quantidade processos.
  -MaxKeepAliveRequests: deve ser menor que maxclient
  -desabilitar o módulo status: a2dismod status
  -Teste de performance, instalar apache2-utils
  -1000 acessos e 20 requisições simultâneas: ab -n 1000 -c 20 http://www.usp.br 
  -KeepAliveTimeout 15 -> para 3?