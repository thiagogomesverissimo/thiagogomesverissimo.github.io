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

<hr />
Formação Acadêmica
==================

<ul>
  <li> <a href="http://www.teses.usp.br/teses/disponiveis/43/43134/tde-20072016-161023/publico/mestradoThiagoGomesVerissimo2016IFUSP.pdf">
    Mestre em Física, Universidade de São Paulo, 2016
    <i class="fa fa-file-pdf-o"></i></a>
  </li>
  <li> <a href="#">
    Graduação em Licenciatura em Física, Universidade de São Paulo, 2009
    <i class="fa fa-file-pdf-o"></i></a>
  </li>
</ul>

<hr />
Apresentações realizadas
========================

<ul>
    {% for item in site.talks %}
        <li> <b> <a href="{{base_path}}/{{ item.url }}">{{ item.title }}</a> </b><br> {{ item.content}}</li>
    {% endfor %}
</ul>

<hr />
Cursos ministrados
==================

<ul>
    {% for item in site.teaching %}
      <li> <a href="{{base_path}}/{{ item.url }}">{{ item.title }} </a></li>
    {% endfor %}
</ul>

<hr />
Publicações
===========

<ul>
   {% for item in site.publications %}
       <li> <a href="{{base_path}}/{{ item.url }}">{{ item.title }} </a> </li>
   {% endfor %}
</ul>

<hr />
Participações em eventos (como ouvinte)
=======================================

<b>2015</b>
<ul>
  <li> <a href="{{base_path}}/files/certificados/eventos/2015/iag-bigdata.pdf">
    I Workshop sobre Ciência de Dados do IAG/USP 
    <i class="fa fa-file-pdf-o"></i></a>
    <br> Instituto de Astronomia, Geofísica e Ciências Atmosféricas da Universidade de São Paulo. 4h40.
  </li>
</ul>

<hr />
Cursos realizados
=================

<b>2019</b>
<ul>
  <li> <a href="{{base_path}}/files/certificados/cursos/2019/ime-usp-algoritimos-java.pdf">
    Algoritmos em Java.
    <i class="fa fa-file-pdf-o"></i></a>
    <br> Instituto de Matemática e Estatística  da Universidade de São Paulo. 20h.
  </li>
</ul>

<b>2017</b>
<ul>
  <li> <a href="{{base_path}}/files/certificados/cursos/2017/4Linux-devops.pdf">
    Infraestrutura ágil com práticas DEVOPS usando Docker, Git, Jenkins, Puppet e Ansible
    <i class="fa fa-file-pdf-o"></i></a>
    <br> 4Linux. 40h.
  </li>
</ul>

<hr />
Participações em grupos (estudos, pesquisa etc)
===============================================
<ul>
  <li> USPdev </li>
  <li> Flusp </li>
</ul>

