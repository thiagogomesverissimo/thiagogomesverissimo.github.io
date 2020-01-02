---
title: 'Compilação de comandos drush em ambiente multisite'
date: 2019-01-17
permalink: /posts/drush-commands
categories: 
  - tutorial
tags:
  - drupal
  - drush
---

Seleção de comandos drush usados para gerenciamento de centenas de sites
em Drupal com core compartilhado, em especial no ambiente aegir. 
Compilados em conjunto com [Augusto César Freire Santiago](https://github.com/acesarfs) e [Ricardo Fontoura](https://github.com/ricardfo).

Trocar senha do usuário admin para sua senha-secreta:

{% highlight bash %}
site='exemplo.com'
drush @$site user-password admin --password='senha-secreta'
{% endhighlight %}

Listar temas desabilitados de um site:

{% highlight bash %}
drush @[site] pml --status=disabled --type=theme --pipe
{% endhighlight %}

Listar módulos desabilitados de um site:

{% highlight bash %}
site=exemplo.usp.br
drush @$site pml --status=disabled --type=module --pipe
{% endhighlight %}

Mesma listagem acima, mas com o resultado em uma única linha:

{% highlight bash %}
site=exemplo.usp.br
drush @$site pml --status=disabled --type=module --pipe | tr -s '\n' ' '
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

Configurar usuário 1 com username admin:

{% highlight bash %}
site='exemplo.com'
drush @$site sql-query "update users set name='admin' where uid=1"
{% endhighlight %}

## Específicos para Drupal 8

Verificar se um tema específico está como default em algum site *.exemplo.com:

{% highlight bash %}
tema='adaptivetheme'
for site in $(ls sites/ | grep *.exemplo.com);
do 
  echo "Verificando $site"; 
  drush @$site cget system.theme default | grep $tema; 
done
{% endhighlight %}

Apagar qualquer configuração referente a um módulo específico.
Muito útil para quando a pasta do módulo foi removida e a ausência da mesma
está quebrando o site. Por exemplo, vamos usar o webform:

{% highlight bash %}
site='exemplo'
for i in $(drush @$site cli | grep webform);do 
  drush @$site config-delete $i;
done
drush @$site cache-rebuild
{% endhighlight %}

Atualizar banco de dados depois de atualização: 
{% highlight bash %}
ls /sites/all/modules > /tmp/lista.txt 
for i in $(cat /tmp/lista | grep fflch.usp.br); do drush updb -l http://$i -y; done
{% endhighlight %}

Criar lista de módulos que não são do core
{% highlight bash %}
drush pml --no-core --type=module --status="enabled" --pipe > /tmp/modules.txt
{% endhighlight %}

Listar módulos e temas desabilidados:
{% highlight bash %}
drush pm-list --no-core --status="disabled,not installed" --pipe -l http://modelod7.fflch.usp.br
{% endhighlight %}

Habilitar módulos e temas desabilitados
{% highlight bash %}
drush en `drush pm-list --status="disabled,not installed" --pipe -l http://grafica.fflch.usp.br` -l http://grafica.fflch.usp.br
{% endhighlight %}

