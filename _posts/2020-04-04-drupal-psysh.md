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

Você pode acessar o Drupal e programar em php iterativo 
usando drush ou drupal console:

{% highlight bash %}
drush php
# ou
drupal shell
{% endhighlight %}

## Coleções de códigos

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

