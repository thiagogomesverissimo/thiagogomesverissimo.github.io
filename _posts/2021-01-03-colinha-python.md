---
title: 'Colinha Python'
date: 2021-01-03
permalink: /posts/colinha-python
categories: 
  - python
tags:
  - python
---

## Trabalhando com datas

Lendo uma data de uma string, calculando a diferença com hoje e mostrando
a idade aproximada: 
{% highlight python %}
from datetime import datetime
nascimento = datetime.strptime('10/11/1986 19:36:00','%d/%m/%Y %H:%M:%S')
delta = datetime.today() - nascimento
print(delta.days/365)
{% endhighlight %}

Convertendo data para string:
{% highlight python %}
from datetime import datetime
hoje = datetime.today()
print(hoje.strftime('%d/%m/%Y %H:%M:%S'))
{% endhighlight %}

## notebook jupiter
{% highlight python %}
%matplotlib inline
{% endhighlight %}

{% highlight python %}
%timeit minha_funcao()
{% endhighlight %}
