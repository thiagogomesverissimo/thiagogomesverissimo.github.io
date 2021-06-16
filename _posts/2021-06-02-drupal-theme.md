---
title: 'Criando um Tema para Drupal'
date: 2021-06-02
permalink: /posts/drupal-theme
categories:
  - tutorial
tags:
  - drupal
---

Conversão não exaustiva de um site estático para um tema do Drupal.

<ul id="toc"></ul>

## Site estático

Vou selecionar o site estático *learn-educational-free-responsive-web-template* disponível em https://github.com/learning-zone/website-templates
Chamaremos nosso tema de educational.

## assets encontrados na index.html

- assets/css/bootstrap.min.css
- assets/css/font-awesome.min.css
- assets/css/bootstrap-theme.css
- assets/css/da-slider.css
- assets/css/style.css

- assets/js/modernizr-latest.js
- assets/js/jquery.cslider.js
- assets/js/custom.js

- assets/images/logo.png

- assets/images/spotlight.jpg
- assets/images/ny.png
- assets/images/news1.jpg
- assets/images/news2.jpg
- assets/images/news3.jpg
- assets/images/news4.jpg

## Regiões e arquivo info

Vou definir as seguintes regiões: content, middle1, middle2, middle3, bottom e footer
Tirar um print do estilo e chamar de screenshot.png

educational.info.yml

{% highlight yml %}
name: educational
type: theme
description: 'educational example'
core_version_requirement: ^8 || ^9

base theme: classy

libraries:
  - educational/global-styles-and-scripts

regions:
  content: Conteúdo
  menu: menu
  middle1: middle1
  middle2: middle2
  middle3: middle3
  bottom: bottom
  footer: rodapé
{% endhighlight %}

## Estilos e Javascript

educational.libraries.yml

{% highlight yml %}
global-styles-and-scripts:
  css:
    theme:
      assets/css/bootstrap.min.css: {}
      assets/css/font-awesome.min.css: {}
      assets/css/bootstrap-theme.css: {}
      assets/css/da-slider.css: {}
      assets/css/style.css: {}
  js:
    assets/js/modernizr-latest.js: {}
    assets/js/jquery.cslider.js: {}
    assets/js/custom.js: {}
{% endhighlight %}

## templates

Renomear index.html para templates/page.html.twig

Blocos serão definidos dessa maneira:

{% highlight html %}
{% raw %}
  {{ page.content }}
  {% if page.middle2 %}
    {{ page.middle2}}
  {% endif %}
{% endraw %}
{% endhighlight %}

## menu
web/core/modules/system/templates/menu.html.twig

{% highlight html %}
{% raw %}
<ul class="nav navbar-nav pull-right mainNav">
  {% for item in items %}
    <li>{{ link(item.title, item.url) }}</li>
  {% endfor %}
</ul>
{% endraw %}
{% endhighlight %}


## configurações do tema  

falta fazer

## logo

falta fazer