Atualização método 1: 
 - Não baixa as imagens
 - php tools/upgrade.php patch
 - php tools/upgrade.php upgrade 

Atualização Método 2: 
 - Download and decompress the package from the OJS web site
 - Make a copy of the config.inc.php provided in the new package
 - Move or copy the following files and directories from your current OJS installation:
        - config.inc.php
        - public/
        - Your uploaded files directory ("files_dir" in config.inc.php), if it
          resides within your OJS directory
 - php tools/upgrade.php upgrade

Consultas:
 SELECT count(issue_id) FROM `issues`;
 SELECT count(article_id) FROM `articles` 
 SELECT count(journal_id) FROM `journals` where `enabled` =1 ;
 SELECT count(author_id) FROM `authors`;
 SELECT count(user_id) FROM `users`;
 update article_settings set setting_value=NULL  
   where setting_name='title' and (setting_value='TITULO NULO' or setting_value=' TITULO NULO');

Importações/Exportações
 php importExport.php list
 php importExport.php UserImportExportPlugin import myfile.xml minharevista continue_on_error

.htaccess 
  <IfModule mod_rewrite.c>
     RewriteEngine on
     RewriteCond %{REQUEST_FILENAME} !-d
     RewriteCond %{REQUEST_FILENAME} !-f
     RewriteRule ^(.*)$ index.php/$1 [QSA,L]
   </IfModule>

cron do OJS: 
  28 0 10 * * * php /var/www/ojs/tools/runScheduledTasks.php

Captcha
  /usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf

Configuração do Apache2
  <VirtualHost *:80>
    DocumentRoot /var/www/ojs
    ServerName revistas.usp.br
    ServerAlias ojs.example.org  www.ojs.example.org
    RewriteEngine On
    RewriteOptions inherit
  </VirtualHost>

