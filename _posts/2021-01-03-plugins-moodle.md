---
title: 'Plugins Moodle'
date: 2021-01-03
permalink: /posts/plugins-moodle
tags:
  - moodle
---

O sucesso de um software depende muito do quão podemos modificá-lo para atender
nossas necessidades particulares. Do ponto de vista de desenvolvimento, eu sempre
olho para um framework através da sua estrutura de API e hooks. As classes do moodle, 
na sua versão atual, 3.x, me lembra muito o Drupal 5.x ou 6.x e portanto não segue muito
a estrutura de frameworks modernos como symfony, laravel ou o próprio Drupal 9.x.
De qualquer modo, segue-se uma série de anotações referente ao desenvolvimento de plugins
para o moodle.

<ul id="toc"></ul>

## Criando o plugin

O moodle trabalha com tipos de plugins. Cada tipo de plugin deve ser colocado
no diretório correspondente. Existe um tipo genérico chamado `local` onde criarei
meu primeiro plugin. Chamo de genérico, pois quero fazer uma mudança que não está 
relacionada a estrutura de um curso, mas sim relacionada a parte administrativa
da instância. 
Nosso plugin interceptará a renderização de strings na camada de template 
deixando tudo em maiúscula, o chamaremos de `tudoupper`.
Crie o diretório do plugin:

{% highlight shell %}
mkdir -p local/tudoupper
{% endhighlight %}

Importante: todos arquivos do plugin devem conter: `defined('MOODLE_INTERNAL') || die();`.

Os arquivos mínimos para o moodle reconhecer nosso plugin são:

[version.php](https://docs.moodle.org/dev/version.php) com metadados do plugin:
{% highlight php %}
<?php
defined('MOODLE_INTERNAL') || die();
$plugin->component = 'local_tudoupper'; // Nome do plugin
$plugin->version = 2021010300; //  YYYYMMDDXX
{% endhighlight %}

O outro arquivo obrigatório é o do idioma, no qual devemos ao menos
especificar o `pluginname`:
{% highlight shell %}
mkdir -p local/tudoupper/lang/en
touch local/tudoupper/lang/en/local_tudoupper.php
{% endhighlight %}

{% highlight php %}
<?php
defined('MOODLE_INTERNAL') || die();
$string['pluginname'] = 'Plugin que deixa tudo maiúsculo';
{% endhighlight %}

Neste momento, ao acessar o moodle como `site administrator` o sistema
reconhecerá e habilitará nosso plugin. 

### String API

Grande parte das classes que no geral vamos querer alterar em um plugin
do tipo `local` estão em `lib/classes`. Queremos interceptar a classe que
renderiza string para o template, assim vamos na busca de uma interface
que trare de string:

{% highlight shell %}
find ./lib/classes -iname "*string*"
{% endhighlight %}

Identificamos a interface `./lib/classes/string_manager.php` que é 
implementada pela classe `./lib/classes/string_manager_standard.php`. 
Há um método chamado `get_string` com a descrição: Get String 
returns a requested string.

No nosso plugin criaremos um diretórios chamado `classes`:
{% highlight shell %}
mkdir -p local/tudoupper/classes
touch local/tudoupper/classes/tudoupper_string_manager.php
{% endhighlight %}

Em tudoupper_string_manager.php vamos extender core_string_manager_standard
e sobrescrever o método get_string() copiando sua assinatura assim como
definida na interface:

{% highlight php %}
<?php
namespace local_tudoupper;
defined('MOODLE_INTERNAL') || die();
class tudoupper_string_manager extends \core_string_manager_standard {
  public function get_string($identifier, $component = '', $a = null, $lang = null) {
    $string = parent::get_string($identifier, $component, $a , $lang );
    return strtoupper($string);
  }
}
{% endhighlight %}

Conforme a [documentação](https://docs.moodle.org/dev/String_API) informamos
ao moodle no `config.php` para usar nossa classe ao invés da `core_string_manager_standard`:

{% highlight php %}
$CFG->customstringmanager = '\local_tudoupper\tudoupper_string_manager';
{% endhighlight %}

No `version.php` podemos subir a versão do nosso plugin:
{% highlight php %}
$plugin->version = 2021010301;
{% endhighlight %}

## Composer

Posso estar enganado, mas não encontrei até o momento uma maneira de definir
globalmente em um projeto moodle que usarei composer e que portanto as dependências
dos meus plugins devem ser baixadas. Não é a melhor prática, mas vamos inicializar
nosso plugin como um projeto composer distribuindo o diretório 
`vendor` junto se necessário. Vou instalar uma biblioteca chamada `jawira/case-converter`:

{% highlight shell %}
cd local/tudoupper/
composer init
composer require jawira/case-converter
{% endhighlight %}

Agora vamos modificar tudoupper_string_manager para usar essa biblioteca:

{% highlight php %}
<?php
namespace local_tudoupper;

defined('MOODLE_INTERNAL') || die();
require_once($CFG->dirroot . '/local/tudoupper/vendor/autoload.php');

use Jawira\CaseConverter\Convert;

class tudoupper_string_manager extends \core_string_manager_standard {
  public function get_string($identifier, $component = '', $a = null, $lang = null) {
    $string = parent::get_string($identifier, $component, $a , $lang );
    $obj = new Convert($string);
    return $obj->toCamel();
  }
}
{% endhighlight %}





