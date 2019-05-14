---
title: 'Múltiplos envios de e-mails a partir de uma template'
date: 2019-05-13
permalink: /posts/multiplos-emails
categories: 
  - tutorial
tags:
  - mutt
  - msmtp
---

Quando realizamos procedimentos repetitivos no computador sempre
da aquela sensação de que algo está errado, pois o computador existe
exatamente para isso: repetir.
Vou dar uma dica bem prática para quando queremos enviar individualmente emails
para uma lista de pessoas trocando poucos elementos no corpo da mensagem. 
Esse é um típico exemplo de tarefa que existem muitas maneiras para automatizá-la e
aqui optei por uma bem simplista, usando apenas o *mutt* e um pequeno script em
shell. Começamos instalando o mutt:

{% highlight bash %}
    sudo apt-get install mutt
{% endhighlight %}

Se você ainda não usa o mutt (deveria), segue uma configuração mínima,
que deve estar em *~/.muttrc* e que o torna capaz de enviar emails usando smtp:

{% highlight bash %}
set use_from=yes
set realname="Seção Xurepinhas Anônimos"
set from="exemplo@gmail.com"
set envelope_from=yes
set smtp_url="smtp://yourusername@smtp.example.com:587/"
set smtp_pass="Your1!Really2@AweSome3#Password"
{% endhighlight %}

A seguir temos um template de e-mail, chamado de email.txt, no qual queremos 
trocar apenas os valores `__nome__` e `__tamanho__` a depender do destinatário.

{% highlight bash %}
Prezado(a) __nome__

A Seção Xurepinhas Anônimos vem informar por meio deste a desativação 
do antigo sistema de armazenamento de arquivos. 
Seus arquivos totalizam `__tamanho__` GB e devem ser retirados imediatamente
do servidor central.

Atenciosamente,
Jéssica Xurepa
{% endhighlight %}

Na lista abaixo a primeira coluna corresponde a um número, que vamos injetar em
`__tamanho__`. A segunda coluna é o nome da pessoa e a última coluna 
o(s) e-mails do destinatário.

{% highlight bash %}
46|Alexandre Pereira|ale@hotmail.com, alea@yahoo.com.br
40|Augusto Pimpolho|augusto@gmail.com, augu2@gmail.com
31|Maria Dantas|marimari@gmail.com
{% endhighlight %}

Por fim, o script.sh abaixo configura o delimitador da nossa lista
para *pipe*, lê nosso template email.txt, faz as substituições
necessárias e dispara os e-mails para cada pessoa da sua lista.

{% highlight bash %}
#!/bin/bash
IFS="|"; 
while read f1 f2 f3; 
do 
    body=$(cat email.txt| sed "s/__nome__/$f2/g" | sed "s/__tamanho__/$f1/g")
    echo $body | mutt -s "URGENTE - Seus Arquivos Pessoais" $f3
done < lista.txt

{% endhighlight %}

Daqui para frente, basta adaptá-lo conforme suas necessidades.






