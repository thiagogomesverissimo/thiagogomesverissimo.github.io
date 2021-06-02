---
title: 'Criando um Tema para Drupal'
date: 2021-01-26
permalink: /posts/drupal-theme
categories:
  - tutorial
tags:
  - drupal
---

Conversão não exaustiva de um site estático para um tema do Drupal.

<ul id="toc"></ul>

## 0 - Site estático

Vou selecionar o site estático *learn-educational-free-responsive-web-template* disponível em https://github.com/learning-zone/website-templates
Chamaremos nosso tema de educational.

## 1 - Regiões e arquivo info

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
  middle1: middle1
  middle2: middle2
  middle3: middle3
  bottom: bottom
  footer: rodapé
{% endhighlight %}

## 2 - Estilos e Javascript

educational.libraries.yml

{% highlight yml %}
global-styles-and-scripts:
  css:
    theme:
      assets/bootstrap.min.css: {}
      css/style.css: {}
  js:
    assets/bootstrap.min.js: {}

  dependencies:
    - core/jquery

{% endhighlight %}

## 3 - templates

Renomear index.html para templates/page.html.twig

Blocos serão definidos dessa maneira: **{{ page.content }}** ou **{{ page.footer }}**

## 4 - logo

## 5 - menu

## 6 - configurações do tema  