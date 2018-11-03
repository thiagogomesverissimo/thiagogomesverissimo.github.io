Title: Aegir - Entregando instâncias Drupal sob demanda
Date: 2014-12-03 10:20
Modified: 2010-12-05 19:30
Category: Tutorial
Tags: Drupal
Slug: aegir
Status: draft
Authors: Thiago Gomes Veríssimo
Summary: Minha experiência com uso de Drupal

Boas práticas
 -Clonar o site full para nova plataforma antes de migrar para ver se os módulos são compatíveis
 -Alterações no settings.php: criar um local.settings.php (não fechar php ?>)
 -Acessar com usuário do Aegir: su -s /bin/bash - aegir 
 -drush vdel hosting_queue_cron_running
 -se alguma tarefa fallhar, copiar o comando drush do log e rodar com --debug
 -Rodar comando do root, mas como aegir:
   -su -s /bin/bash aegir -c 'drush | grep provision'
 -alguns erros são causado por causa do limite de memória do php-cli


Instalação manual - MySQL
 -mysql-server 
 -/etc/my.cnf configurar: bind-address
 -sudo mysql_secure_installation
 -GRANT ALL PRIVILEGES ON *.* TO 'aegir_root'@'ip_do_apache' IDENTIFIED BY 'password' WITH GRANT OPTION;

Instalação manual - Apache2
 -apache2 php5 php5-cli php5-gd php5-mysql php-pear postfix sudo rsync git-core unzip
 -/etc/hosts (ip real) e etc/hostname
 -adduser --system --group --home /var/aegir aegir
 -adduser aegir www-data  #Coloca o aegir no grupo www-data
 -a2enmod rewrite
 -criar arquivo: /etc/sudoers.d/aegir e colocar as duas linhas abaixo:
     Defaults:aegir !requirett
     aegir ALL=NOPASSWD: /usr/sbin/apache2ctl 
 -chmod 0440 /etc/sudoers.d/aegir
 -pear channel-discover pear.drush.org
 -pear install drush/drush-4.5.0 (pois o aegir só funciona em drush 4)
 -Se tornar aegir: su -s /bin/bash - aegir
 -drush dl --destination=/var/aegir/.drush provision-6.x
 -Entrar em /var/aegir/.drush 
 -drush hostmaster-install 
    --aegir_db_host='10.2.2.1' 
    --aegir_db_user='aegir_root' 
    --aegir_db_pass='password' 
    --client_email='mail@example.org' 
    --client_name='fflch' 
 -ln -s /var/aegir/config/apache.conf /etc/apache2/conf.d/aegir.conf
 -Para backup, entre em: /var/aegir/hostmaster-x.x
 -drush dl hosting_backup_gc hosting_backup_queue

Migração:
 -Sincronize as plataformas entre os dois aegir, excluindo os sites (*usp.br) da pasta sites: 
 -rsync --recursive 
        --stats 
        --progress 
        --delete 
        --update 
        --links 
        --compress 
        --perms 
        --exclude="*usp.br*" 
        --rsh="ssh -p45222" 
        /var/aegir/platforms/ root@example.org:/var/aegir/platforms
 -Exemplo de geração de backup com 3 comandos:
 -drush @example.usp.br provision-backup
 -drush provision-save '@example.usp.br' 
   --context_type=site 
   --platform=@platform_drupal628 
   --uri='example.usp.br' 
   --db_server=@server_10.2.2.211 
   --client_name=fflch
 -drush @example.usp.br provision-deploy /var/aegir/migrate/example.tar.gz
 -Falta continuar com os passos da importação no outro server.



