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

