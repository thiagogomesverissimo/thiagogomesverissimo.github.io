---
title: 'Coleção de tasks para executar no Drupal de forma iterativa'
date: 2020-03-23
permalink: /posts/drupal-psysh
categories:
  - tutorial
tags:
  - drupal
---

Programar no Drupal pela linha de comando de uma forma iterativa
nos facilita a vida quando precisamos executar tarefas que são pontuais 
e que não vale a pena preparar um módulo para tal.

<ul id="toc"></ul>

# Formas de acesso ao Drupal cli

Você pode acessar o Drupal e programar em php iterativo 
usando drush ou drupal console:
{% highlight bash %}
drush php
# ou
drupal shell
{% endhighlight %}

Caso use o aegir:
{% highlight bash %}
drush @seusite.com.br php
{% endhighlight %}

## Dump de um node

Carregando um node com nid 3 e dando um dump:
{% highlight bash %}
$node = \Drupal::entityTypeManager()->getStorage('node')->load(3);
dump($node)
{% endhighlight %}

## Corrigindo o formato do campo boby

Carregando todos nodes do tipo *ficha* e alterando o campo *body->format* para
*full_html*:
{% highlight bash %}
$nids = \Drupal::entityQuery('node')->condition('type','ficha')->execute();
$nodes = \Drupal\node\Entity\Node::loadMultiple($nids);

foreach ($nodes as $node) {
    $node = \Drupal::entityTypeManager()->getStorage('node')->load($node->nid->value);
    $node->body->format = 'full_html';
    $node->save();
}
{% endhighlight %}


## Corrigindo o formato do campo field_resumo para múltiplos tipos de conteúdos

Carregando todos nodes do tipo *ficha* e alterando o campo *body->format* para
*full_html*:
{% highlight bash %}

$tipos = ['catalogos','livros',,'producoes_visuais','trabalhos_de_conclusao'];

$nids = \Drupal::entityQuery('node')->condition('type',$tipos, 'IN')->execute();
$nodes = \Drupal\node\Entity\Node::loadMultiple($nids);

foreach ($nodes as $node) {
    $node = \Drupal::entityTypeManager()->getStorage('node')->load($node->nid->value);
    $node->field_resumo->format = 'full_html';
    $node->save();
}
{% endhighlight %}

Se o campo for multivalorado talvez tenha que fazer algo do tipo:

$node->field_resumo[0]->format

ou um loop no campo

## Substituindo string em um campo de todos nodes do mesmo tipo

Dado um tipo de conteúdo chamado `verbete` no qual há um campo 
`field_verbete`, vamos substituir tudo de `antigo.fflch.usp.br`
para `novo.fflch.usp.br`:
{% highlight bash %}
$nids = \Drupal::entityQuery('node')->condition('type','verbete')->execute();
$nodes = \Drupal\node\Entity\Node::loadMultiple($nids);

foreach ($nodes as $node) {
    $node = \Drupal::entityTypeManager()->getStorage('node')->load($node->nid->value);
    $node->field_verbete->value = 
str_replace('antigo.fflch.usp.br','novo.fflch.usp.br',$node->field_verbete->value);
    $node->save();
}
{% endhighlight %}

## Trocando o campo alias

Dado que você tem o objeto `$node` pode trocar a url alternativa dessa forma:
{% highlight bash %}
$node->path->alias = '/novo-caminho-do-node'
$node->path->pathauto = Drupal\pathauto\PathautoState::SKIP;
$node->save();
{% endhighlight %}

# Marcando pais dos termos de taxonomia 

Esse script carrega todos nodes de um tipo de conteúdo chamado `fotos_bd`
que contém um campo que faz referência a termos de taxonomia: `field_descritores`.
Ocorre que esses termos apresentam uma hierarquia entre si, mas somente os termos
filhos estão marcados nos nodes. Esse script procura os termos de que pai e os
marca também. 
{% highlight bash %}
$nids = \Drupal::entityQuery('node')->condition('type','fotos_bd')->execute();
$nodes = \Drupal\node\Entity\Node::loadMultiple($nids);

foreach ($nodes as $node) {
    $node = \Drupal::entityTypeManager()->getStorage('node')->load($node->nid->value);
    $descritores = $node->get('field_descritores');

    # 1. Guardar todos tids, de pais e filhos
    $tids = [];
    foreach ($descritores->referencedEntities() as $descritor) {
        array_push($tids, $descritor->id());
        if($descritor->parent->target_id != 0) {
          array_push($tids, $descritor->parent->target_id);
        }
    }
    $tids = array_unique($tids);

    # 2. monta um array $update com somente os tids que deve ficar
    $update = [];
    foreach($tids as $tid) {
      $update[] = ['target_id' => $tid];
    }

    $node->field_descritores = $update;
    $node->save();
}
{% endhighlight %}

## Manipulating nodes usign Api: 

Nodes are fundamental entities that represent individual pieces of content such as articles, pages, blog posts, and more. The Drupal API provides a powerful set of functions and methods to manipulate nodes programmatically. 

Attach a file to the node:
{% highlight bash %}
<?php 

use \Drupal\node\Entity\Node;
use \Drupal\file\Entity\File;

$data = file_get_contents('/home/thiago/sabrina.pdf');
$file = file_save_data($data, 'public://sabrina.pdf', FILE_EXISTS_REPLACE);

$node = Node::create([
    'type' => 'livros',
    'title' => 'Teste com Sabrina',
    'field_tombo' => 123,
    'field_arquivo' => [
        'target_id' => $file->id(),
        'alt' => 'Pdf com o nome da sabrina',
        'title' => 'Sabrina pdf'
    ],
]);

$node->save();
{% endhighlight %}

Attach multiple files to the node:
{% highlight bash %}
<?php 

use \Drupal\node\Entity\Node;
use \Drupal\file\Entity\File;

$data1 = file_get_contents('/home/thiago/sabrina1.pdf');
$data2 = file_get_contents('/home/thiago/sabrina2.pdf');


$file1 = file_save_data($data1, 'public://sabrina1.pdf', FILE_EXISTS_REPLACE);
$file2 = file_save_data($data2, 'public://sabrina2.pdf', FILE_EXISTS_REPLACE);


$node = Node::create([
    'type' => 'livros',
    'title' => 'Teste com Sabrina 2 arquivos',
    'field_tombo' => 123,
    
    'field_arquivo' => [
        [
            'target_id' => $file1->id(),
            'alt' => 'Pdf 1 com o nome da sabrina',
            'title' => 'Sabrina 1 pdf'
        ],
        [
            'target_id' => $file2->id(),
            'alt' => 'Pdf 2 com o nome da sabrina',
            'title' => 'Sabrina 2 pdf'
        ],
    ],
    

]);

$node->save();
{% endhighlight %}

