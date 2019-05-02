---
layout: archive
title: "Currículo"
permalink: /curriculo/
author_profile: true
redirect_from:
  - /resume
  - /cv
---

{% include base_path %}

***

Formação
========
* Mestre em Física, Universidade de São Paulo, 2016
* Graduação em Licenciatura em Física, Universidade de São Paulo, 2009

Apresentações
=============

  <ul>
    {% for item in site.talks %}
        <li> <a href="{{base_path}}/{{ item.url }}">{{ item.title }} </a></li>
    {% endfor %}
  </ul>

Publicações
===========
  <ul>
   {% for item in site.publications %}
      <li> <a href="{{base_path}}/{{ item.url }}">{{ item.title }} </a></li>
   {% endfor %}
  </ul>
  
Ensino
======
  <ul>
    {% for item in site.teaching %}
      <li> <a href="{{base_path}}/{{ item.url }}">{{ item.title }} </a></li>
    {% endfor %}
  </ul>
  
Grupos
======
<ul>
  <li> USPdev </li>
  <li> Flusp </li>
</ul>

Cursos realizados
=================
<b>2018</b>
<ul>
  <li>DevOps - 4linux</li>
  <li>Bla -Xuxu</li>
</ul>

<b>2017</b>
<ul>
  <li>DevdwedOps - 555</li>
  <li>Bla -ssXuxu</li>
</ul>
  
