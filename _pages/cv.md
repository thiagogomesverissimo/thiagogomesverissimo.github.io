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
<b>2019</b>
<ul>
  <li> <a href="{{base_path}}/files/certificados/2019/ime-usp-algoritimos-java.pdf">
    Algoritmos em Java.
    <i class="fa fa-file-pdf-o"></i></a>
    <br> Instituto de Matemática e Estatística  da Universidade de São Paulo. 20h.
  </li>
</ul>

<b>2015</b>
<ul>
  <li> <a href="{{base_path}}/files/certificados/2015/iag-bigdata.pdf">
    I Workshop sobre Ciência de Dados do IAG/USP 
    <i class="fa fa-file-pdf-o"></i></a>
    <br> Instituto de Astronomia, Geofísica e Ciências Atmosféricas da Universidade de São Paulo. 4h40.
  </li>
</ul>
  
