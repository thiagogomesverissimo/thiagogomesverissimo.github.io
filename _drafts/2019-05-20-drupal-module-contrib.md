---
title: 'Criando módule contrib no Drupal'
date: 2019-05-20
permalink: /posts/drupal-module-contrib
categories:
  - tutorial
tags:
  - drupal
---

https://www.drupal.org/docs/develop/documenting-your-project/help-text-standards



Instalação global do codesniffer
https://www.drupal.org/docs/8/modules/code-review-module/installing-coder-sniffer


verificando se o código está ok

{% highlight bash %}
alias drupalcs="phpcs --standard=Drupal --extensions='php,module,inc,install,test,profile,theme,css,info,txt,md'" alias drupalcsp="phpcs --standard=DrupalPractice --extensions='php,module,inc,install,test,profile,theme,css,info,txt,md'" alias drupalcbf="phpcbf --standard=Drupal --extensions='php,module,inc,install,test,profile,theme,css,info,txt,md'"
{% endhighlight %}

https://www.drupal.org/docs/8/modules/code-review-module/php-codesniffer-command-line-usage


mkdir ~/temp
cd temp
git clone https://git.drupalcode.org/project/pareviewsh
cd pareviewsh
composer install


https://pareview.sh/


