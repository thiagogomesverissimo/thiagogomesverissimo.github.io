---
title: 'Deploy do aegir com ansible: entregue instâncias Drupal na sua instituição'
date: 2018-11-03
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
{: .text-justify}

Nos três CMS a curva de aprendizado inicial é baixa e o tempo despendido desde a instalação
até a configuração mínima para colocarmos um site no ar é pequeno, sendo assim, comum
encontrar pessoas que conseguem publicar seus conteúdos na web, mesmo sem um conhecimento
mais profundo de infraestrutura ou desenvolvimento.
No geral usam hospedagem compartilhada e naturalmente depois que o site está no ar deixam de 
dar atenção as questões técnicas, como aplicação de atualizações de seguranças recomendadas
(que chegam a ser semanais) e passam a de dedicar mais aos conteúdos,  tendo as vezes
seus sites atacados por conta desse cenário.
{: .text-justify}

Em instituições que são grandes e distribuídas, como nos órgãos do governo, os sites podem ou
não compartilhar algumas características, sendo que um sistema que permite o gerenciamento
de múltiplas instâncias de sites no mesmo código é mais vantagoso que o modelo de hospedagem
compartilhada, pois torna mais eficiente a manutenção.
{: .text-justify}

Neste texto, vamos abordar esse cenário com Drupal dando um foco na perspectiva de quem
gerencia a infraestrutura. O Drupal implementa nativamente uma estrutura chamada multisite,
que permite entregarmos instâncias de sites rodando no mesmo core e portanto na mesma versão.
O [aegir](https://www.aegirproject.org/) é um drupal que nos permite gerenciar de forma fácil 
outras instâncias Drupal usando o próprio conceito de multisites, mas tudo via web.
{: .text-justify}

## Ambiente

Esse tutorial foi feito usando como ambiente de desenvolvimento a dupla
virualbox e vagrant. Não é obrigatório usá-los, mas disponibilizo o
Vagrantfile para quem o quiser:

{% highlight ruby  %}
{% include snippets/vagrant/Vagrantfiles/debian %}
{% endhighlight %}

Salve esse código em um arquivo chamado Vagrantfile e na mesma pasta rode:

{% highlight console  %}
vagrant up
vagrant ssh
{% endhighlight %}

No caso, vamos instalar nosso aegir em um máquina de IP 192.168.8.8.
O sistema de multisite do Drupal exige que cada site tenha seu próprio domínio,
mas para finalidade desse tutorial, algumas entradas em */etc/hosts* na nossa 
máquina física (hospedeira) são suficiente:

{% highlight bash %}
192.168.8.8 aegir.xurepinha.net aegir
192.168.8.8 site1.xurepinha.net site1
192.168.8.8 site2.xurepinha.net site2
192.168.8.8 site3.xurepinha.net site3
{% endhighlight %}

## Aegir

Vamos fazer uma primeira instalação do aegir seguindo os comandos recomendados
no [site oficial](https://www.aegirproject.org/#download) do projeto. Acesso
nossa máquina virtual usando *vagrant ssh* e depois *sudo su*. 

{% highlight bash %}
apt-get install apt-transport-https
wget -O /usr/share/keyrings/aegir-archive-keyring.gpg https://debian.aegirproject.org/aegir-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/aegir-archive-keyring.gpg] https://debian.aegirproject.org stable main" | sudo tee -a /etc/apt/sources.list.d/aegir-stable.list
apt-get update
apt-get install aegir3 aegir-archive-keyring 
{% endhighlight %}

No processo de instalação quando for perguntado qual a *URL of the hostmaster
frontend* coloque a mesma url que registramos em */etc/hosts*, 
ou seja: *aegir.xurepinha.net*.

O aegir trabalha com o conceito de plataforma, que nada mais é
que o core do drupal em conjunto com os módulos, temas e bibliotecas.  
Os sites rodam em cima das plataformas, possibilitando ter no 
mesmo ambiente versões de drupal diferentes.
Para tal, baixe as versões do drupal que irá trabalhar na pasta
*/var/aegir/platforms/* manualmente, com drush ou com composer.
Por exemplo, vamos instalar as versões 8.6.0 e 8.6.1.

{% highlight bash %}
cd /var/aegir/platforms/
# Opção 1: usando drush
drush dl drupal-8.6.0
drush dl drupal-8.6.1
# Opção 2: usando composer
composer create-project drupal/drupal drupal-8.6.0 8.6.0
composer create-project drupal/drupal drupal-8.6.1 8.6.1
{% endhighlight %}

O usuário default é admin, vamos definir uma senha também *admin* para 
acessarmos nosso aegir pela web:

{% highlight bash %}
sudo su aegir
drush @hostmaster user-password admin --password='admin'
{% endhighlight %}

No seu navegador acesse *http://aegir.xurepinha.net* com usuário e senha
admin/admin. 

## Instalação do aegir usando ansible

Podemos automatizar esse processo de instalação usando
o ansible, vamos então remover a VM criada anteriormente
e criá-la novamente.

{% highlight bash %}
vagrant destroy -f
vagrant up
{% endhighlight %}

Agora vamos criar um diretório e os arquivos mínimos que permitirão
provisionar o aegir com o ansible

{% highlight bash %}
mkdir deploy-aegir-with-ansible
cd deploy-aegir-with-ansible
touch hosts ansible.cfg playbook.yml
{% endhighlight %}

Configuração do 

{% highlight bash %}
[defaults]
allow_world_readable_tmpfiles = True
inventory = ./hosts
roles_path = ./roles
{% endhighlight %}

{% highlight bash %}
[aegir]
192.168.8.8 ansible_connection=ssh ansible_user=vagrant ansible_ssh_private_key_file="~/.vagrant.d/insecure_private_key"
{% endhighlight %}


{% highlight bash %}
ansible-galaxy install geerlingguy.php-versions geerlingguy.php geerlingguy.composer geerlingguy.mysql ergonlogic.aegir
{% endhighlight %}


{% highlight yml %}
{% include snippets/playbook_aegir.yml %}
{% endhighlight %}

{% highlight bash %}
ansible-playbook playbook.yml
{% endhighlight %}

{% highlight bash %}
{% endhighlight %}
## Gerenciando seus sites requisições API

