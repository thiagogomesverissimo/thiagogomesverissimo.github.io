---
title: 'Migração Aegir entre Servidores'
date: 2021-09-17
permalink: /posts/migrate-aegir
tags:
  - github
---

Vamos copiar os sites do *aegir velho* para o *aegir novo*.


## No servidor velho

- Desabilitar fila de backup automático em hosting->tasks 
- Zerar a pasta /var/aegir/backups

variáveis de ambiente
{% highlight shell %}
export platform=drupal8916a
export sites=$(ls /var/aegir/platforms/$platform/web/sites | grep fflch.usp.br)
{% endhighlight %}

Colocando sites offline e fazendo backups para migração:

{% highlight shell %}
for site in $sites
do
  drush @$site sset system.maintenance_mode 1 --yes
  drush @$site provision-backup
done
{% endhighlight %}


Move o diretório /var/aegir/backups para o novo servidor:

scp -r /var/aegir/backups root@192.168.8.93:/var/aegir/aegir_antigo

## No servidor novo

chown -R aegir: /var/aegir/aegir_antigo

export db='server_192.168.8.57'
export profile='fflchprofile'
export platform_name=platform_drupal8916a


export arquivos=$(ls /var/aegir/aegir_antigo)
for arquivo in $arquivos
do
  site=$(echo $arquivo | cut -d'-' -f1)

  drush provision-save @$site --context_type=site --platform=@$platform_name --uri=$site --db_server=@$db --aliases=www.$site --redirection=0 --profile=$profile --client_name=admin
  drush @$site provision-deploy /$arquivo
done

drush @hostmaster hosting-task @$platform_name verify

Colocar o site online:

export platform=drupal8916a
export sites=$(ls /var/aegir/platforms/$platform/web/sites | grep fflch.usp.br)
for site in $sites
do
  drush @$site sset system.maintenance_mode 0 --yes
done

TODO: Habilitar sites na nova plataforma


Deletar os sites no aegir antigo:

No servidor antigo:

for site in $sites
do
  drush @hostmaster hosting-task @$site delete
done


{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}

{% highlight shell %}
{% endhighlight %}
