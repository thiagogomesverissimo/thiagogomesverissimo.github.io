---
title: 'Tópicos em Samba'
date: 2020-04-10
permalink: /posts/topicos-em-samba
categories:
  - tutorial
tags:
  - samba
---

Criando um servidor samba como domain controller (DC):

Dado o ip 192.168.7.202:

- Em /etc/hostname: samba.proaluno.usp.br
- Em /etc/hosts adicione a linha: 127.0.1.1 samba samba.proaluno.usp.br




Instalação de pacotes:

{% highlight bash %}
apt -y install samba krb5-config krb5-user libnss-winbind libpam-winbind winbind samba smbclient ldb-tools samba-common
{% endhighlight %} 

Provisionando a base de dados samba-ad-dc com o usuário Administrator com senha Pr0Aluno123:

{% highlight bash %}
rm /etc/samba/smb.conf
samba-tool domain provision --server-role=dc --dns-backend=SAMBA_INTERNAL --realm='PROALUNO.USP.BR' --domain='PROALUNO' --adminpass='Pr0Aluno123' --use-rfc2307
cp /var/lib/samba/private/krb5.conf /etc/
{% endhighlight %}

Desabilitar smbd nmbd winbind:
{% highlight bash %}
systemctl stop smbd nmbd winbind
systemctl disable smbd nmbd winbind
{% endhighlight %} 

Habilitar serviço samba-ad-dc:
{% highlight bash %}
systemctl unmask samba-ad-dc
systemctl start samba-ad-dc
systemctl enable samba-ad-dc 
{% endhighlight %}   

Desabilitando complexidade de senhas:
{% highlight bash %}
samba-tool user setexpiry Administrator --noexpiry 
samba-tool domain passwordsettings set --complexity=off
samba-tool domain passwordsettings set --history-length=0
samba-tool domain passwordsettings set --min-pwd-age=0
samba-tool domain passwordsettings set --max-pwd-age=0
samba-tool domain passwordsettings set --min-pwd-length=0
{% endhighlight %}  

Criando um grupo chamado ALUNOGR com um usuário 666666:
{% highlight bash %}
samba-tool group add ALUNOGR
samba-tool user create 666666
samba-tool group addmembers ALUNOGR 666666
samba-tool group listmembers ALUNOGR
{% endhighlight %}  

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

Listar computadores do domínio:

{% highlight bash %}
pdbedit --list | grep "\$$"
{% endhighlight %}


Remover computador do domínio:
{% highlight bash %}
pdbedit -x -m NAME_OF_COMPUTER_TO_REMOVE
{% endhighlight %}

Mudar o home do usuario maria de */home/maria* para
*\\dominio.com\maria* e mudar ponto de montagem
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
