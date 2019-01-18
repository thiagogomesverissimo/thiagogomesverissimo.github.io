---
title: 'Compilação de comandos cups'
date: 2019-01-17
permalink: /posts/cups-commands
categories: 
  - tutorial
tags:
  - cups
---

Compilação de comandos que já me livraram de tarefas repetitivas
quando preciso imprimir algo.

Listar impressoras instaladas:

{% highlight bash %}
lpstat -a
{% endhighlight %}

Enviar arquivo para impressão usando *nome_da_impressora* listado acima:

{% highlight bash %}
lp -d nome_da_impressora ~/docs/arquivo.pdf
{% endhighlight %}

Imprimir todos arquivos pdf de uma pasta estando nela:

{% highlight bash %}
IFS=$'\n'; for i in $(ls | grep pdf);do lp -d nome_da_impressora $i;done
{% endhighlight %}

Enviar arquivo para impressão com papel A4, frente e verso e não deixando espaços
vazios nas margens:

{% highlight bash %}
lp -d nome_da_impressora -o sides=two-sided-long-edge -o fit-to-page -o media=A4 ~/docs/arquivo.pdf
{% endhighlight %}


Enviando para impressão arquivo no formato paisagem (landscape). O padrão é 
retrato (portrait):

{% highlight bash %}
lp -d nome_da_impressora -o landscape ~/docs/arquivo.pdf
{% endhighlight %}

Enviando para impressão 30 cópias do mesmo documento:

{% highlight bash %}
lp -n 30 -d nome_da_impressora ~/docs/arquivo.pdf
{% endhighlight %}

Enviando para impressão apenas as páginas 1,2,8,10,11 e 12 de um documento:

{% highlight bash %}
lp -d nome_da_impressora -o page-ranges=1-2,8,10-12 ~/docs/arquivo.pdf
{% endhighlight %}
lp  filename


