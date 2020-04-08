---
title: 'Redirecionando portas para outras máquinas com iptables'
date: 2020-04-08
permalink: /posts/redirecionar-portas-iptables
tags:
  - debian
---

O script abaixo é usado no cenário em que temos equipamentos
em uma rede inválida, no exemplo 10.88.0.0/24, onde todos respondem
com um serviço http na porta 80.
Temos uma máquina com ip público 1.2.3.4 que também se comunica com a rede inválida.
Queremos criar o seguintes ambiente de redirecionamento:

{% highlight bash %}
1.2.3.4:40002 -> 10.88.0.2:80
1.2.3.3:40003 -> 10.88.0.3:80
...
1.2.3.4:40019 -> 10.88.0.19:80
...
1.2.3.4:40255 -> 10.88.0.255:80
{% endhighlight %}

ps. Lembre-se de habilitar o ipv4/ip_forward no seu sistema operacional.

{% highlight bash %}
#!/bin/bash
iptables -F
iptables -t nat -F

ip_publico=1.2.3.4

# accept everything
iptables -A INPUT -j ACCEPT;
iptables -A FORWARD -j ACCEPT;
iptables -A OUTPUT -j ACCEPT;

for i in $(seq -f "%03g" 2 255)
do
        j=$(echo $i | sed 's/^0*//')
        iptables -t nat -A PREROUTING -p tcp --dport 40${i} -j DNAT --to-destination 10.88.0.${j}:80
        iptables -t nat -A POSTROUTING -p tcp -d 10.88.0.${j} --dport 80 -j SNAT --to-source ${ip_publico}
done
{% endhighlight %}
