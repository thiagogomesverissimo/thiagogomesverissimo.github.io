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
  <li> 2016: Mestre em Física, Universidade de São Paulo.
    <a href="http://www.teses.usp.br/teses/disponiveis/43/43134/tde-20072016-161023/publico/mestradoThiagoGomesVerissimo2016IFUSP.pdf"><i class="fa fa-file-pdf"></i></a>
  </li>
  <li>
    2009: Graduação em Licenciatura em Física, Universidade de São Paulo.
  </li>
</ul>
 
## Apresentações

{% include cv/talks.md %}

## Cursos e Eventos (como ouvinte)
 
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
