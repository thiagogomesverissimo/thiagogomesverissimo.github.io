---
title: 'Compilação de alguns comandos drush em ambiente multisite'
date: 2019-01-17
permalink: /posts/drush-commands
categories: 
  - tutorial
tags:
  - drupal
  - drush
---

Listar nomes dos módulos desabilitados de um site:

{% highlight bash %}
site=exemplo.usp.br
drush @$site pml --status=disabled --type=module --pipe
{% endhighlight %}

Listar na mesma linha nomes dos módulos desabilitados de um site:

{% highlight bash %}
site=exemplo.usp.br
drush @$site pml --status=disabled --type=module --pipe | tr -s '\n' ' '
{% endhighlight %}

Listar temas desabilitados de um site:
{% highlight bash %}
drush @[site] pml --status=disabled --type=theme --pipe
{% endhighlight %}

## Específicos para Drupal 7

Desinstalar todos os módulos desabilitados de todos os sites *.exemplo.com:

{% highlight bash %}
for site in $(ls sites/ | grep exemplo.com);
do 
  echo "Desabilitando módulos no $site"; 
  modules=$(drush @$site pml --status=disabled --type=module --pipe | tr -s '\n' ' '); 
  drush @$site pmu $modules -y; 
done
{% endhighlight %}

Verificar se um tema específico está como default em algum site *.exemplo.com:

{% highlight bash %}
tema='adaptivetheme'
for site in $(ls sites/ | grep *.exemplo.com);
do 
  echo "Verificando $site"; 
  drush @$site cget system.theme default | grep $tema; 
done
{% endhighlight %}

Verificar quais temas estão habilitados em todos sites *.exemplo.com:

{% highlight bash %}
for site in $(ls sites/ | grep exemplo.com); 
do 
  echo $site; 
  drush @$site pml --status='enabled' --type='theme' --format=list; 
done
{% endhighlight %}

Desinstalar o tema em todos os sites:
{% highlight bash %}
for site in $(ls sites/ | grep exemplo.com); 
do
  drush @$i pm-uninstall $tema -y; 
done
{% endhighlight %}

Módulos que estão na plataforma p1 e não estão na p2:

{% highlight bash %}
diff  p1/sites/all/modules/ p2/sites/all/modules/ | grep "Only in p1" | cut -d':' -f2
{% endhighlight %}

Configurar usuário 1 com username admin e senha adminpass:

    site='exemplo.com'
    drush @$site sql-query "update users set name='admin' where uid=1"
    drush @$site user-password fflch --password='adminpass'

