---
title: 'Desenvolvendo módulos para Drupal'
date: 2020-03-23
permalink: /posts/drupal-modules
categories:
  - tutorial
tags:
  - drupal
---

Pacotes básicos para instalar o Drupal no seu debian usando sqlite3:

{% highlight bash %}
apt-get install php php-common php-cli php-gd php-curl php-xml php-mbstring php-sqlite3 sqlite3
{% endhighlight %}

Instalação do composer globalmente:
{% highlight bash %}
curl -s https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer
{% endhighlight %}

Criando uma instalação limpa para começar a desenvolver. Será criado um
diretório chamado projetodev, sendo usuário/senha igual a admin/admin:

{% highlight bash %}
composer create-project drupal-composer/drupal-project:8.x-dev projetodev --no-interaction
cd projetodev
./vendor/bin/drupal site:install standard --db-type="sqlite" \
       --site-name="Ambiente Dev" --site-mail="dev@locahost" \
       --account-name="admin" --account-pass="admin" --account-mail="dev@localhost" \
       --no-interaction
{% endhighlight %}

Subindo um server local para desenvolvimento:

{% highlight bash %}
./vendor/bin/drupal serve -v
{% endhighlight %}

Caso precise zerar o banco e começar tudo novamente:
{% highlight bash %}
rm web/sites/default/files/.ht.sqlite*
{% endhighlight %}

Desligando o cache durante o desenvolvimento:
{% highlight bash %}
./vendor/bin/drupal site:mode dev
{% endhighlight %}

Religando o cache:
{% highlight bash %}
./vendor/bin/drupal site:mode prod
{% endhighlight %}


./vendor/bin/drupal site:mode dev

## Dicas para configurar seu ambiente

Alias para colocar no seu bashrc:

{% highlight bash %}
alias drupalcs="phpcs --standard=Drupal --extensions='php,module,inc,install,test,profile,theme,css,info,txt,md'" 
alias drupalcsp="phpcs --standard=DrupalPractice --extensions='php,module,inc,install,test,profile,theme,css,info,txt,md'" 
alias drupalcbf="phpcbf --standard=Drupal --extensions='php,module,inc,install,test,profile,theme,css,info,txt,md'"
{% endhighlight %}

Usando pareviewsh localmente (mesmo efeito de usar
pelo site https://pareview.sh/):

{% highlight bash %}
mkdir ~/temp
cd temp
git clone https://git.drupalcode.org/project/pareviewsh
cd pareviewsh
composer install
{% endhighlight %}

## Links importantes:

 - [Padrões de escrita de códigos](https://www.drupal.org/docs/develop/documenting-your-project/help-text-standards)
 - [Instalação global do codesniffer](https://www.drupal.org/docs/8/modules/code-review-module/installing-coder-sniffer)
 - [Usando codesniffer por linha de comando](https://www.drupal.org/docs/8/modules/code-review-module/php-codesniffer-command-line-usage)


