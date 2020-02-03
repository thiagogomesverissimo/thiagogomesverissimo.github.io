---
title: 'Minha colinha de comandos'
date: 2020-02-02
permalink: /posts/colinha-de-comandos
tags:
  - debian
---

Segue-se minha colinha de comandos no gnu/linux, em especial no debian, para tarefas corriqueiras:

Configurar expiração de conta do usuário em uma data:
 
{% highlight bash %}
usermod -e "September 20, 2014" USUARIO
{% endhighlight %}

Compactando com tar.gz: 

{% highlight bash %}
tar -vzcf files.tar.gz /home/thiago/files
tar -vzjf files.tar.gz /home/thiago/files
{% endhighlight %}

Descompactar arquivo em bzip2:

{% highlight bash %}
tar -vjxf file.tar.bz2
{% endhighlight %}
 
Programar reboot daqui a seis horas: 

{% highlight bash %}
shutdown -r +6:00
{% endhighlight %}

Fazer usuário a trocar senha no próximo login:

{% highlight bash %}
chage -d 0 USUARIO
{% endhighlight %}  
    
Fazer usuário trocar de senha a cada 60 dias:

{% highlight bash %}
chage -M 60 bianca
{% endhighlight %}
    
Deletar usuário e home:
{% highlight bash %}
deluser thiago --remove-home
{% endhighlight %}

Reparando partição:

{% highlight bash %}
fsck.ext4 /dev/sda1
{% endhighlight %}
 
Remontar partição sem precisar reinicar:

{% highlight bash %}
mount -o remount rw /particao
{% endhighlight %}

Listagem de arquivos ordenada por tamanho:
{% highlight bash %}
ls -lS
{% endhighlight %}

Move diretório Desktop/mygits para repos? (não me lembor):
{% highlight bash %}
find . -type f -exec sed -i "s/Desktop\/mygits/repos/g" {} \;
{% endhighlight %}

Muda hostname sem precisar reiniciar:
{% highlight bash %}
hostnamectl set-hostname sti-035374
{% endhighlight %}

Teclado ABNT2:
{% highlight bash %}
setxkbmap -model abnt2 -layout br
{% endhighlight %}
