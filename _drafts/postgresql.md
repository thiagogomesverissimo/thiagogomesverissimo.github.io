Implementação PostgreSQL:

  apt-get install postgresql
 
É interssante separar a partição:
  /var/lib/postgresql/9.1/main/pg_xlog 
  -Lembrar que o dono/grupo da nova partição será postgres e permissão 0700.  

Locales

  dpkg-reconfigure locales -> en_US.UTF-8 UTF-8
  -Em postgresql.conf 
    lc_messages = 'en_US.UTF-8'
  -Para usar resultados de logs no pgbadger: 
    log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d '
    log_checkpoints = on
    log_connections = on
    log_disconnections = on
    log_lock_waits = on
    log_temp_files = 0
   -Em postgresql.conf:  
      wal_level =archive   
      archive_mode=on 
      archive_command='cp -i %p /postgresql/pitr/arquivamento/%f < /dev/null'

Backup PITR
  -criar usuário admin como superuser sem senha; 
  -no pg_hba.conf (local all admin trust). 
  /etc/init.d/postgresql restart
  psql -U admin postgres -c "SELECT pg_start_backup('meu_backup_postgresql')"
  cp -a /var/lib/postgresql/9.1/main/* /backup/pitr/inicial/
  psql -U admin postgres -c "SELECT pg_stop_backup()"

Dump
  -Tudo
    pg_dumpall -U admin > /bkp/postgresql/postgresql_full.sql
  -Indiviudal
    pg_dump -U thiago meubanco -h localhost > /tmp/meudump.sql

Restauração usando um novo cluster: 
 -Criar novo cluster
 -Apagar postmaster.pid /opts
 -Mudar porta
 -Copiar pg_hba.conf
 -Zerar pg_xlog
 -Criar arquivo recovery.conf 
   restore_command = 'cp /postgresql/newcluster/arquivamento/%f "%p"')
 -subir o banco: pg_ctl -D /cluster start
 
Conectar no Banco
  \c nome_do_banco 

Listar tabelas
 \d 

Acessar tabela
 \d minha_tabela

Criar usuário
  CREATE USER thiago PASSWORD 'senha';

Alterar senha
  ALTER USER thiago WITH PASSWORD 'nova_senha';
  ALTER USER thiago with encrypted password 'senha';

Criar banco e dar pemissão para usuário
 CREATE DATABASE mydb
   WITH TEMPLATE = template0 
   ENCODING = 'UTF8' 
   LC_COLLATE = 'pt_BR.UTF-8' 
   LC_CTYPE = 'pt_BR.UTF-8' 
   owner thiago;

Importar arquivo CSV 
 -Não colocar cabeçalho no arquivo, 
 -As colunas devem estarem na mesmo ordem que as colunas da chamada
   COPY tabela_no_banco(coluna1,coluna2) FROM '/tmp/file.csv' WITH DELIMITER AS ',' CSV;


Adminitração com phppgadmin
  sudo apt-get install phppgadmin
  -Em /etc/phppgadmin/apache.conf
      allow from 143.107.8.0/255.255.255.0 ::1/128
  -Por padrão o usuário principal não loga pelo modo grafico, fazer:
  -Em /usr/share/phppgadmin/conf/config.inc.php
    $conf['extra_login_security'] = false;



