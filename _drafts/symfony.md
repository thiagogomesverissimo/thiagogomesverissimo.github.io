# Configuração local da máquina de desenvolvimento:

Instalação dos pacotes básicos:

    sudo apt-get -y install php php-xml php-intl php-mbstring
    sudo apt-get -y install php-pgsql

Instalação do symfony:

    sudo curl -LsS https://symfony.com/installer -o /usr/local/bin/symfony
    sudo chmod a+x /usr/local/bin/symfony

Instalação do composer:

    wget https://getcomposer.org/installer
    php installer
    sudo mv composer.phar /usr/local/bin/composer
    rm installer

Para o symfony é obrigatório configurar o timezone, assim, inserir a linha 
abaixo em /etc/php/7.0/fpm/php.ini:

    date.timezone = "America/Sao_Paulo"

Instalação do nodejs e do bower:

    curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
    sudo apt-get install -y nodejs
    sudo npm install -g bower

Depois de todas dependências instaladas, para iniciar um novo projeto com 
symfony, basta:

    symfony new meu_projeto

Configurar o usuário, nome do banco de dados, ip e senha em 
*app/config/parameters.yml* e inserir nos parâmetros
(necessário configurar a VM do banco de dados, veja como abaixo):

    database_driver: pdo_pgsql
    database_host: 192.168.100.71
    database_port: 5432
    database_name: fflch
    database_user: fflch
    database_password: fflch

Parametrizar o driver do banco de dados que vem por padrão o mysql. Trocar a 
primeira linha abaixo pela segunda em *app/config/config.yml*:

    driver: pdo_mysql
    driver: "%database_driver%"

Subir um servidor local para testes:

    cd meu_projeto
    php bin/console server:start

## Banco de dados 

Se possível, separe a máquina do postgresql:

    sudo dpkg-reconfigure locales # pt_BR.UTF8
    sudo apt-get install postgresql 
    
Criação de super usuário e db:

    sudo su
    su postgres
    psql
    CREATE USER fflch WITH PASSWORD 'fflch';
    CREATE DATABASE fflch OWNER fflch;

Criação de super usuário *administrador*:

    sudo su
    su postgres
    psql
    CREATE USER administrador WITH PASSWORD 'minhasenha';
    ALTER USER administrador WITH SUPERUSER;

Para liberar acesso externo na máquina do postgresql em 
*/etc/postgresql/9.5/main/pg_hba.conf* insira:

    host    all             all             0.0.0.0/0            md5

E em */etc/postgresql/9.5/main/postgresql.conf* insira:

    listen_addresses = '*'

Restartar o serviço:

    service postgresql restart

Na máquina local, teste o acesso ao postgresql:

    sudo apt-get -y install postgresql-client
    psql -U fflch postgres  -h 192.168.100.71 -W
    
# symfony 

Criação de entidade e cd templates/form:

    cd meu_projeto
    php bin/console doctrine:generate:entity --entity=AppBundle:Equipamento
    php bin/console generate:doctrine:crud --entity=AppBundle:Equipamento --route-prefix=equipamento --with-write -n

Gerar funções getters e setters para o novo campo:

    php bin/console doctrine:generate:entities AppBundle

    
Na pasta do projeto, iniciar o bower:

    bower init

Criar um arquivo *.bowerrc* na raiz do projeto com o conteúdo:

    { "directory": "web/assets/vendor/" }

Colocar web/assets/vendor/ no .gitignore.

    echo "/web/assets/vendor/" >> .gitignore 

Instalar o jquery, bootstrap e fontawesome a partir do bower:

    bower install --save jquery
    bower install --save jquery-ui
    bower install --save bootstrap
    bower install --save fontawesome
    bower install --save ckeditor

Na seção do twig em *app/config/config.yml* renderizar os formulários com
bootstrap:

    form_themes:
        - bootstrap_3_layout.html.twig
    
Há dois tipos de relação *One to Many* e *many to many*. 
Vamos criar uma entidade rede, e cada equipamento 
só pode pertencer a uma rede, mas uma rede pode conter muitos equipamentos: 

    php bin/console doctrine:generate:entity --entity=AppBundle:Rede --fields="nome:string(length=20)" -n
    php bin/console generate:doctrine:crud --entity=AppBundle:Rede --route-prefix=rede --with-write -n

Na entidade Rede, adicionar o campo equipamentos em *src/AppBundle/Entity/Rede.php*
e o método *__toString*, executado na construção do formulário de cadastro de
equipamentos:

    /**
     * @ORM\OneToMany(targetEntity="Equipamento",mappedBy="rede")
     * @ORM\OrderBy({"createdat"="DESC"}) 
     */
    private $equipamentos;
    
    public function __toString()     
    {
        return $this->getNome();
    } 

Na entidade Equipamento, adicionar o campo rede *src/AppBundle/Entity/Equipamento.php*:

    /**
     * @ORM\ManyToOne(targetEntity="Rede", inversedBy="equipamentos")
     */
    private $rede;

Gerar funções getters e setters para os novos campos nas duas entidades
(perceba que na função getEquipamento um objeto é retornado):

    php bin/console doctrine:generate:entities AppBundle:Equipamento
    php bin/console doctrine:generate:entities AppBundle:Rede

Ainda na maneira *bruta*, mas por enquanto, aplicar no banco:

    php bin/console doctrine:database:drop --force
    php bin/console doctrine:database:create 
    php bin/console doctrine:schema:update --force

Adicionar o campo rede no array $builder *src/AppBundle/Form/EquipamentoType.php*.
Adicionar a coluna rede (equipamento.rede) na tabela geral da entidade de equipamentos
*app/Resources/views/equipamento/index.html.twig*. 


TODO: encaixar no texto:
Na relação ManyToOne, quando obrigatória:  @ORM\JoinColumn(nullable=false)



