---
title: 'Tópicos em Samba'
date: 2020-04-10
permalink: /posts/topicos-em-samba
categories:
  - tutorial
tags:
  - samba
---

Compilação de comandos que mais uso no samba

Obrigar a *maria* a trocar senha no próximo login:
{% highlight bash %}
pdbedit --pwd-can-change-time=0 maria
{% endhighlight %}

No windows, promover usuária maria do AD como admin local
{% highlight bash %}
net localgroup administradores NºUSP /add
{% endhighlight %}

Ver as configurações completas:

{% highlight bash %}
pdbedit -Lv > /tmp/saida.txt
{% endhighlight %}

Ver configurações do usuário *maria*:

{% highlight bash %}
pdbedit -Lv maria
{% endhighlight %}

Remover computador do domínio:

{% highlight bash %}
pdbedit -x -m NAME_OF_COMPUTER_TO_REMOVE
{% endhighlight %}

Mudar o home do usuario maria de /home/maria para
\\dominio.com\maria e mudar ponto de montagem
para H:

{% highlight bash %}
pdbedit -h "\\\\dominio.com\\maria" -D "H:" maria
{% endhighlight %}

Para que a senha do usuário expire a cada 30 dias e ele seja obrigado a
mudá-la:
{% highlight bash %}
pdbedit -P "maximum password age" -C 2592000
{% endhighlight %}

Desabilitar expiração de senha para o usuário Administrator:
{% highlight bash %}
samba-tool user setexpiry Administrator --noexpiry 
{% endhighlight %}

Desabilitar complexidade da senha:
{% highlight bash %}
samba-tool domain passwordsettings set --complexity=off
{% endhighlight %}

O usuário só possa mudar a senha após 25 dias depois da última
troca:
{% highlight bash %}
pdbedit -P "minimum password age" -C 2160000
{% endhighlight %}

Tamanho mínimo de senha de 8 caracteres:
{% highlight bash %}
pdbedit -P "min password length" -C 8
{% endhighlight %}

Mantém um histórico de senhas usadas pelo usuário para que ele não possa
reutiliza-las.
Neste caso ele não poderá utilizar as últimas duas senhas.
{% highlight bash %}
pdbedit -P "password history" -C 2
{% endhighlight %}

A senha de root não expira:
{% highlight bash %}
pdbedit -c "[X ]" -u root
{% endhighlight %}

Script para obrigar todos os usuários do samba a trocarem
suas senhas:
{% highlight bash %}
#!/bin/bash

for USUARIO in $(pdbedit -L | grep -v \'$:\'| grep -v \'root:\' | cut -d:
-f1)
do
   pdbedit --pwd-must-change-time=0 $USUARIO
   pdbedit --pwd-can-change-time=0 $USUARIO

done
{% endhighlight %}
