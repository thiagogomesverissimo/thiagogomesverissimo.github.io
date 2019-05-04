---
title: 'Deploy do aegir com ansible: entregue instâncias Drupal na sua instituição'
date: 2019-03-21
permalink: /posts/deploy-aegir-com-ansible
header:
  teaser: "images/aegir.jpg"
categories: 
  - tutorial
tags:
  - ansible
  - aegir
---

Na última década explodiram as opções de ferramentas para publicação de conteúdos na web,
em especial, os que permitiam a criação e manutenção rápida de pequenos sites ou portais institucionais.
Os Sistema de Gerenciamento de Conteúdo (ou Content Management System – CMS) foram protagonistas
neste cenário e três deles fizeram e fazem muito sucesso até hoje: Drupal, Joomla e Wordpress.

Nos três CMS's a curva de aprendizado inicial é baixa e o tempo despendido desde a instalação
até a configuração mínima para colocarmos um site no ar é pequeno, sendo assim, comum
encontrar pessoas que conseguem publicar seus conteúdos na web, mesmo sem conhecimento
profundo de infraestrutura ou desenvolvimento.
No geral, usam hospedagens compartilhadas e naturalmente depois que o site está no ar, deixam de 
dar atenção as questões técnicas, como aplicação de atualizações de seguranças recomendadas
(que chegam a ser semanais) e passam a se dedicar mais aos conteúdos, cenário que eventualmente
propicia aumento das chances desses sites serem atacados.

Em grandes instituições e em especial as geograficamente distribuídas, como nos órgãos do governo, 
os sites de setores internos podem ou não compartilhar algumas características, 
sendo que um sistema que permite o gerenciamento de múltiplas instâncias de sites no mesmo código 
é mais vantajoso que o modelo de hospedagem compartilhada, pois torna mais eficiente a 
manutenção por parte da equipe de infraestrutura.

Neste texto, vamos abordar esse cenário com Drupal dando um foco na perspectiva de quem
gerencia a infraestrutura. O Drupal implementa nativamente uma estrutura chamada multisite,
que permite entregarmos instâncias de sites independentes no conteúdo, mas rodando no mesmo 
core.
O [aegir](https://www.aegirproject.org/) é um software desenvolvido em drupal que nos permite 
gerenciar de forma fácil outras instâncias Drupal usando o próprio conceito de multisites, 
sendo que administração dessas instâncias pode ser feita via terminal ou pela web.


## Criando um ambiente básico de desenvolvimento

Para seguir esse tutorial uso-se no ambiente de desenvolvimento a dupla
virualbox e  vagrant. Não é obrigatório usá-los, mas disponibilizo o
Vagrantfile da máquina virtual (VM) com a parametrização mínima para instalação
do aegir usando Debian:

{% highlight ruby  %}
{% include snippets/Vagrantfiles/debian %}
{% endhighlight %}

Crie um diretório e salve esse código em um arquivo chamado Vagrantfile.
Com o comando *vagrant up* criaremos a VM e com *vagrant ssh* conectaremos 
na máquina via ssh.

{% highlight shell %}
$ mkdir aegir-tutorial
$ cd aegir-tutorial
$ touch Vagrantfile # inserir conteúdo do Vagrantfile acima
$ vagrant up
$ vagrant ssh
{% endhighlight %}

Nossa VM vai subir com IP 192.168.8.8, que pode ser alterado no Vagrantfile.
O sistema de multisite do Drupal exige que cada site tenha seu próprio domínio,
mas para finalidade desse tutorial, algumas entradas em */etc/hosts* na nossa 
máquina física (hospedeira) são suficiente:

{% highlight bash %}
# Algumas entradas em /etc/hosts
192.168.8.8 aegir.xurepinha.net aegir
192.168.8.8 site1.xurepinha.net site1
192.168.8.8 site2.xurepinha.net site2
192.168.8.8 site3.xurepinha.net site3
{% endhighlight %}

## Aegir

Há duas formas de instalação do aegir: manual ou usando um repositório.
No [site oficial do aegir](https://www.aegirproject.org/#download)
há informações de como adicionar o repositório que permite então 
instalarmos o aegir usando o apt:

{% highlight console %}
# apt-get install aegir3 aegir-archive-keyring
{% endhighlight %}

No processo de instalação, quando for perguntado qual a *URL of the hostmaster
frontend* coloque uma das urls que registramos em */etc/hosts*,como por exemplo: 
*aegir.xurepinha.net*. Depois de instalado, pode-se trocar a senha
do usuário admin (criado pelo aegir) usando drush:

{% highlight bash %}
sudo su aegir
drush @hostmaster user-password admin --password='admin'
{% endhighlight %}

No seu navegador acesse *http://aegir.xurepinha.net* com usuário e senha
admin. 

O aegir trabalha com o conceito de plataforma, que nada mais é
que o core do drupal em conjunto com os módulos, profiles, temas e bibliotecas.
Os sites rodam em cima das plataformas, e o servidor aegir nos permite
gerenciar múltiplas plataformas e portanto conseguimos gerenciar no mesmo 
ambiente diferentes versões de drupal.
Para tal, baixe as versões do drupal que irá trabalhar na pasta
*/var/aegir/platforms/* manualmente ou com drush. Pela interface,
vá na opção criar plataforma, coloque o caminho do drupal baixado,
como por exemplo */var/aegir/platforms/drupal-8.6.1* e voilà! 
Adicione sites na plataforma recém criada depois módulos, temas etc.

A versão empacotada do aegir instala versões do php, apache2 e drush
e outras dependências. Na instalação manual descrita no 
[site oficial](https://docs.aegirproject.org/install/)
temos mais controle das versões das dependências, o que é muito mais prático na era
do Drupal 8 onde exige-se cada vez mais versões mais recentes do php.
Os passos na instalação manual são muitos e é importante fazê-los ao menos uma vez. 
Uma vez que a instalação manual é dominada, podemos automatizá-la
usando ferramentas que executam tarefas em um servidor, processo chamado 
de provisionamento. Vamos usar o ansible para esta finalidade.

## Instalação do aegir usando ansible

Vamos deletar nosso ambiente e recriá-lo usando ansible.
Remova a VM criada anteriormente e crie-a novamente.
Se estiver usando vagrant, esses sãos os comandos:

{% highlight bash %}
vagrant destroy -f
vagrant up
{% endhighlight %}

Instale o ansible na sua máquina hospedeira como indicado na
documentação [oficial](https://ansible.com).
Vamos criar os arquivos mínimos que nos permitirão provisionar 
o aegir com o ansible:

{% highlight bash %}
$ touch hosts ansible.cfg playbook.yml
{% endhighlight %}

Conteúdo do arquivo *ansible.cfg*:

{% highlight bash %}
[defaults]
allow_world_readable_tmpfiles = True
inventory = ./hosts
roles_path = ./roles
{% endhighlight %}

Conteúdo do arquivo *hosts*:

{% highlight bash %}
[aegir]
192.168.8.8 
[aegir:vars]
ansible_connection=ssh
ansible_user=vagrant
ansible_ssh_private_key_file="~/.vagrant.d/insecure_private_key"
{% endhighlight %}

No ansible, colocamos a receita para construção do nosso servidor em um playbook.
Podemos especificar tarefa por tarefa no playbook do que deve ser feito ou podemos
agrupar, idealmente semanticamente, essa tarefas em uma role e chamar essa role
a partir do playbook. 

Assim, uma role passa a ser simplesmente um agrupamento de tarefas, no intuito
de encapsular um procedimento de instalação e/ou configuração de algum software. 

Existem muitas roles espalhadas pela web que fazem *N* coisas e 
antes de desenvolver a sua própria é sempre bom procurar para verificar
se não tem alguma role que faça exatamente o que você quer ou pelo menos
que seja ponto de partida para alcançar seu objetivo.

Vamos usar algumas roles famosas e delegar a instalação de dependências 
mínimas para nosso servidor aegir.
Começando pelo apache, vamos baixar a role geerlingguy.apache 
usando o comando ansible-galaxy:

{% highlight bash %}
$ mkdir roles
$ ansible-galaxy install geerlingguy.apache
{% endhighlight %}

Agora criaremos nosso playbook e instalaremos o apache
no nosso servidor. 
Crie um arquivo playbook.yml e coloque o seguinte conteúdo:

{% highlight yml %}
---
- name: playbook que instala um servidor aegir
  become: yes
  hosts: aegir
  roles:
    - geerlingguy.apache
{% endhighlight %}

E para rodar o playbook e fazer o provisionamento do servidor:

{% highlight bash %}
$ ansible-playbook playbook.yml
{% endhighlight %}

A próxima role que vamos adicionar permite que nosso servidor trabalhe
com múltiplas versões do php:

{% highlight bash %}
$ ansible-galaxy install geerlingguy.php-versions
{% endhighlight %}

Na role anterior, apenas instalamos o apache com as configurações
defaults definidas pela role, que podem ser conferidas nas variáveis
definidas em defaults/main.yml.
Na role php-versions, vamos sobrescrever as configurações defaults, pois queremos escolher 
a versão do php como 7.2. Assim, configuraremos uma variável que específica
a versão do php, no caso, php_version, como definido em defaults/main.yml:

{% highlight yml %}
---
- name: playbook que instala um servidor aegir
  become: yes
  hosts: aegir
  vars:
    # geerlingguy.php-versions
    php_version: '7.2'
  roles:
    - geerlingguy.apache
    - geerlingguy.php-versions
{% endhighlight %}

A role *geerlingguy.php* instala de fato o php e em conjunto
vamos baixar a role *geerlingguy.composer* para também instalar
composer na sequência, por sinal, o ansible irá executar as roles
na sequência que elas são declaradas no playbook.

{% highlight bash %}
$ ansible-galaxy install geerlingguy.php geerlingguy.composer
{% endhighlight %}

E novamente vamos controlar o que a role *php* deve 
ou não fazer sobrescrevendo variáveis defaults. Para 
a role composer não vamos alterar nada.

{% highlight yml %}
---
- name: playbook que instala um servidor aegir
  become: yes
  hosts: aegir
  vars:
    # geerlingguy.php-versions
    php_version: '7.2'
    # geerlingguy.php
    php_default_version_debian: '7.2'
    php_use_managed_ini: false
    php_packages_extra:
      - php{{ php_default_version_debian }}-mysql
  roles:
    - geerlingguy.apache
    - geerlingguy.php-versions
    - geerlingguy.php
    - geerlingguy.composer
{% endhighlight %}

Até o momento o aegir só suporta mysql e usaremos 
a role *geerlingguy.mysql*.
É uma prática provisionar esse servidor mysql em outro servidor,
assim faríamos um outro playbook,
mas por questão de praticade, vamos usar o mesmo playbook e portanto
mesmo servidor. 

{% highlight bash %}
$ ansible-galaxy install geerlingguy.mysql
{% endhighlight %}

Vamos criar um superusário do mysql chamado *aegir_root* 
que será usado pelo aegir para gerenciar
os bancos de dados das instâncias dos sites entregues por ele.

{% highlight yml %}
---
- name: playbook que instala um servidor aegir
  become: yes
  hosts: aegir
  vars:
    # geerlingguy.php-versions
    php_version: '7.2'
    # geerlingguy.php
    php_default_version_debian: '7.2'
    php_use_managed_ini: false
    php_packages_extra:
      - php{{ php_default_version_debian }}-mysql
    # geerlingguy.mysql
    mysql_users:
      - name: aegir_root
        host: "localhost"
        password: "aegir_root"
        priv: "*.*:ALL,GRANT"
  roles:
    - geerlingguy.apache
    - geerlingguy.php-versions
    - geerlingguy.php
    - geerlingguy.composer
    - geerlingguy.mysql
{% endhighlight %}

Neste estágio, nosso servidor está completamente preparado
para a instalação do aegir. Dependendo do seu cenário, talvez
você queira escrever uma role para fazer a configuração e
instalação do aegir.

Quando trabalhamos com ansible é muito provável
que você encontre roles que implementam parte daquilo
que precisamos, no caso do aegir, 
[@GetValkyrie](https://github.com/GetValkyrie/)
implementou uma [role](https://github.com/GetValkyrie/ansible-role-aegir)
que instala e configura o aegir, mas não é atualizada desde 2015.
Olhei os muitos forks que existem dessa role e o mantido pelo
[ergonlogic](https://github.com/ergonlogic),
no meu ponto de vista mantém a [role](https://github.com/ergonlogic/ansible-role-aegir) 
mais completa para o aegir.

Um passo adicional que essa role não faz, por enquanto,
é a criação automática de plataformas a partir de projetos
drupal 8 baseados em composer e versionados com git. Assim, criei um 
[fork](https://github.com/thiagogomesverissimo/ansible-role-aegir)
da role do [ergonlogic](https://github.com/ergonlogic) com essa
implementação, que vamos usar aqui.

{% highlight bash %}
$ ansible-galaxy install thiagogomesverissimo.aegir
{% endhighlight %}

Assim, finalmente chegamos ao playbook completo para 
instalação e configuração do aegir, que pode ser modificado
conforme suas necessidades e seu ambiente.

{% highlight yml %}
---
- name: playbook que instala um servidor aegir
  become: yes
  hosts: aegir
  vars:
    # geerlingguy.php-versions
    php_version: '7.2'
    # geerlingguy.php
    php_default_version_debian: '7.2'
    php_use_managed_ini: false
    php_packages_extra:
      - php{{ php_default_version_debian }}-mysql
    # geerlingguy.mysql
    mysql_users:
      - name: aegir_root
        host: "%"
        password: "aegir_root"
        priv: "*.*:ALL,GRANT"
    # aegir
    aegir_db_user: 'aegir_root'
    aegir_db_password: 'aegir_root'
    aegir_frontend_url: 'aegir.xurepinha.net' 
    aegir_additional_packages:
      - libapache2-mod-php{{ php_default_version_debian }}
    aegir_install_git_platforms: true
    aegir_git_platforms:
      - name: master
        repo: https://github.com/fflch/drupal8.git
        version: master
  roles:
    - geerlingguy.apache
    - geerlingguy.php-versions
    - geerlingguy.php
    - geerlingguy.composer
    - geerlingguy.mysql
    - thiagogomesverissimo.aegir
{% endhighlight %}
