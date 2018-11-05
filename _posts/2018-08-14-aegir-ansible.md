---
title: 'Deploy do aegir com ansible: entregue instâncias Drupal na sua instituição'
date: 2018-11-03
permalink: /posts/deploy-aegir-com-ansible
header:
  teaser: "images/aegir.jpg"
categories: 
  - tutorial
tags:
  - ansible
  - aegir
---

Na última década explodiram as opções de ferramentas para publicação de conteúdos na web,
em especial, os que permitiam a criação e manutenção rápida de sites e portais institucionais.
Os Sistema de Gerenciamento de Conteúdo (ou Content Management System – CMS) foram protagonistas
neste cenário e três deles fizeram e fazem muito sucesso até hoje: Drupal, Joomla e Wordpress.

Nos três CMS a curva de aprendizado inicial é baixa e o tempo despendido desde a instalação
até a configuração mínima para colocarmos um site no ar é pequeno, sendo assim, comum
encontrar pessoas que na tentativa de colocar um conteúdo na internet, mesmo sem um conhecimento
mais profundo de infraestrutura ou desenvolvimento conseguem publicar seus conteúdos na web.
No geral usam hospedagem compartilhada e não aplicam as atualizações de seguranças recomendadas
(que chegam a ser semanais) e costumam ter seus sites atacados por conta desse cenário.

Em instituições que são grandes e distribuídas, caso de órgãos do governo, os sites podem ou
não compartilhar algumas característica, assim manter, por exemplo, 500 sites, no modelo hospedagem
compartilhada começa a se tornar uma dor de cabeça, pois imaginem aplicar atualizações semanais em
500 sites!

Neste texto, vamos abordar um pouco sobre o Drupal sob a perspectiva de quem gerencia a 
infraestrutura. O Drupal implmenteta nativamente uma estrutura chamada multisite, que permite mantermos
de cara todas nossas instâncias na mesma versão. 

## Instalação do aegir

O aegir é uma distribuição drupal que nos permite gerenciar de forma fácil outras instâncias Drupal de forma fácil usando o próprio conceito de multisite default no core do Drupal. 

## Instalação do aegir usando ansible

## Gerenciando seus sites requisições API

