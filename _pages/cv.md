---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

Educação
======
* Mestre em Física, Universidade de São Paulo, 2016
* Graduação em Licenciatura em Física, Universidade de São Paulo, 2009

Experiência
======
* Analista de Sistema na Universidade de São Paulo
  * Desenvolvimento 
  * Infraestrutura
  * Gerente de redes

Habilidades
======
* Análises multivariadas
* Desenvolvimento
  * PHP
  * Python
  * Java

Publicações
======
  <ul>{% for post in site.publications %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
  
Palestras
======
  <ul>{% for post in site.talks %}
    {% include archive-single-talk-cv.html %}
  {% endfor %}</ul>
  
Ensino
======
  <ul>{% for post in site.teaching %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
  
Grupos
======
* Atualmente membro do USPdev
