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

<ul id="toc"></ul>

## Formação Acadêmica

<ul>
  <li> Mestre em Física, Universidade de São Paulo, 2016
    <a href="http://www.teses.usp.br/teses/disponiveis/43/43134/tde-20072016-161023/publico/mestradoThiagoGomesVerissimo2016IFUSP.pdf">a <i class="far fa-file-pdf"></i></a>
  </li>
  <li>
    Graduação em Licenciatura em Física, Universidade de São Paulo, 2009
    <i class="far fa-file-pdf"></i>
  </li>
</ul>

 
## Apresentações em eventos,  cursos ministrados

<ul>
    {% for item in site.talks %}
        <li> <b> <a href="{{ item.slides }}">{{ item.title }} <i class="fa fa-link"></i> </a> </b><br> {{ item.content}}</li>
    {% endfor %}
</ul>

## cursos e eventos (ouvinte)
 
{% include cv/ouvinte.md %}
 
## Participações em coletivos

<ul>
  <li> <a href="https://uspdev.github.io">USPdev - devs da Universidade de São Paulo</a> </li>
</ul>


## Publicações

<ul>
   {% for item in site.publications %}
       <li> <a href="{{ item.paperurl }}">{{ item.date |  date: '%Y' }} - {{ item.title }} </a> </li>
   {% endfor %}
</ul>
