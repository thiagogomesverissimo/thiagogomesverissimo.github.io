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
em especial, os que permitiam a criação e manutenção rápida de sites e portais institucionais.
Os Sistema de Gerenciamento de Conteúdo (ou Content Management System – CMS) foram protagonistas
neste cenário e três deles fizeram e fazem muito sucesso até hoje: Drupal, Joomla e Wordpress.

Nos três CMS a curva de aprendizado inicial é baixa e o tempo despendido desde a instalação
até a configuração mínima para colocarmos um site no ar é pequeno, sendo assim, comum
encontrar pessoas que conseguem publicar seus conteúdos na web, mesmo sem um conhecimento
mais profundo de infraestrutura ou desenvolvimento.
No geral usam hospedagem compartilhada e naturalmente depois que o site está no ar, deixam de 
dar atenção as questões técnicas, como aplicação de atualizações de seguranças recomendadas
(que chegam a ser semanais) e passam a se dedicar mais aos conteúdos, cenário que eventualmente
aumenta as chances de seus sites serem atacados.

Em instituições que são grandes e distribuídas, como nos órgãos do governo, os sites podem ou
não compartilhar algumas características, sendo que um sistema que permite o gerenciamento
de múltiplas instâncias de sites no mesmo código é mais vantagoso que o modelo de hospedagem
compartilhada, pois torna mais eficiente a manutenção por parta da equipe de infraestrutura.

Neste texto, vamos abordar esse cenário com Drupal dando um foco na perspectiva de quem
gerencia a infraestrutura. O Drupal implementa nativamente uma estrutura chamada multisite,
que permite entregarmos instâncias de sites rodando no mesmo core e portanto na mesma versão.
O [aegir](https://www.aegirproject.org/) é um drupal que nos permite gerenciar de forma fácil 
outras instâncias Drupal usando o próprio conceito de multisites, sendo que administração
pode ser feita via terminal ou pela web.
{: .text-justify}

## Ambiente

Esse tutorial foi feito usando como ambiente de desenvolvimento a dupla
virualbox e vagrant. Não é obrigatório usá-los, mas disponibilizo o
Vagrantfile para quem o quiser:

{% highlight ruby  %}
{% include snippets/Vagrantfiles/debian %}
{% endhighlight %}

Crie um diretório e salve esse código em um arquivo chamado Vagrantfile. 
Na mesma pasta rode:

{% highlight shell %}
$ mkdir aegir-tutorial
$ cd aegir-tutorial
$ touch Vagrantfile # inserir conteúdo 
$ vagrant up
$ vagrant ssh
{% endhighlight %}

No nossa Vagrantfile vamos subir uma máquina de IP 192.168.8.8.
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

Para acessa a máquina virtual criada com o vagrant:

{% highlight shell %}
$ vagrant ssh
$ sudo su
{% endhighlight %}

Há duas formas de instalação do aegir: manual ou usando um .deb.
Na instalação usando deb é possível adicionar o repositório informando no 
[site oficial](https://www.aegirproject.org/#download)
do projeto e depois:

{% highlight console %}
# apt-get install aegir3 aegir-archive-keyring
{% endhighlight %}

No processo de instalação quando for perguntado qual a *URL of the hostmaster
frontend* coloque a mesma url que registramos em */etc/hosts*, 
ou seja: *aegir.xurepinha.net*. Depois de instalado, pode-se trocar a senha
do usuário admin (criado pelo aegir) usando drush:

{% highlight bash %}
sudo su aegir
drush @hostmaster user-password admin --password='admin'
{% endhighlight %}

No seu navegador acesse *http://aegir.xurepinha.net* com usuário e senha
admin/admin. 

O aegir trabalha com o conceito de plataforma, que nada mais é
que o core do drupal em conjunto com os módulos, temas e bibliotecas.  
Os sites rodam em cima das plataformas, possibilitando ter no 
mesmo ambiente versões de drupal diferentes.
Para tal, baixe as versões do drupal que irá trabalhar na pasta
*/var/aegir/platforms/* manualmente ou com drush. Pela interface,
vá na opção criar plataforma, coloque o caminho do drupal baixado,
como por exemplo */var/aegir/platforms/drupal-8.6.1* e voilà! Adicione
sites na plataforma criada.

A versão empacotada do aegir instala versões do php, apache2 e drush
e outras dependências. Na instalação [manual](https://docs.aegirproject.org/install/)
temos mais controle das versões das dependências, o que é muito útil na era
do Drupal 8 onde exige-se cada vez mais versões mais recentes do php, por exemplo.
Mas como os passos na instação manual são muitos, vamos usar o ansible para 
instalar e configurar o aegir automaticamente.

## Instalação do aegir usando ansible

Remova a VM criada anteriormente e crie-a novamente.

{% highlight bash %}
vagrant destroy -f
vagrant up
{% endhighlight %}

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
agrupar - semanticamente - essa tarefas em uma role e chamar essa role a partir do 
playbook. Assim, uma passa a ser simplesmente um agrupamento de tarefas, no intuito
de encapsular um procedimento de instalação e/ou configuração de algum software, 
como o aegir. Existem muitas roles espalhadas pela web que fazem N coisas e 
antes de desenvolver a sua própria é sempre bom procurar para verificar
se não tem alguma que faça exatamente o que você quer.
Vamos usar algumas para delegar a instalação de dependências do aegir,
começando pelo apache. Assim, vamos baixar a role geerlingguy.apache 
usando o ansible-galaxy:

{% highlight bash %}
$ mkdir roles
$ ansible-galaxy install geerlingguy.apache
{% endhighlight %}

Agora podemos criar nosso playbook e fazer a instalação do apache
no nosso servidor. Crie um arquivo playbook.yml e coloque o seguinte conteúdo:

{% highlight yml %}
---
- name: playbook que instala um servidor aegir
  become: yes
  hosts: aegir
  roles:
    - geerlingguy.apache
{% endhighlight %}

E para rodar o playbook e fazer a instalação do apache:

{% highlight bash %}
$ ansible-playbook playbook.yml
{% endhighlight %}

A próxima role que vamos adicionar permite que nosso servidor trabalhe
com múltiplas versões do php:

{% highlight bash %}
$ ansible-galaxy install geerlingguy.php-versions
{% endhighlight %}

Mas para essa role vamos configurar uma variável que específica
a versão default do php que vamos usar:

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

A role *geerlingguy.php* instala de fato o php e novamente controlamos
o que a role deve ou não fazer usando variáveis.

{% highlight bash %}
$ ansible-galaxy install geerlingguy.php
{% endhighlight %}

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
{% endhighlight %}

https://github.com/ergonlogic/ansible-role-aegir

{% highlight bash %}
$ ansible-galaxy install thiagogomesverissimo.aegir
{% endhighlight %}


