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

## Exemplo: Plugin de Administração

### Estrutura mínima de um plugin

Instalação moodle

{% highlight bash %}
sudo apt install php php-gd php-curl php-xml php-mbstring php-intl php-mysql curl mariabdb-server
{% endhighlight %}

{% highlight bash %}
composer create-project moodle/moodle moodle-for-plugin-dev
{% endhighlight %}

{% highlight bash %}
cd moodle-for-plugin-dev
php admin/cli/install.php \
  --lang=pt_br \
  --wwwroot='http://0.0.0.0:8000' \
  --dataroot='/home/thiago/moodledata' \
  --dbtype=mariadb \
  --dbhost='localhost' \
  --dbname=moodle \
  --dbuser=master \
  --dbpass=master \
  --fullname=moodledev \
  --shortname=moodledev \
  --adminpass='Admin123*' \
  --non-interactive \
  --agree-license
{% endhighlight %}

{% highlight php %}
@error_reporting(E_ALL | E_STRICT);   
@ini_set('display_errors', '1');

$CFG->debug = E_ALL;
$CFG->debugdisplay = 1;
$CFG->langstringcache = 0;
$CFG->cachetemplates = 0;
$CFG->cachejs = 0;
$CFG->perfdebug = 15;
$CFG->debugpageinfo = 1;
{% endhighlight %}

{% highlight shell %}
php -S 0.0.0.0:8000
{% endhighlight %}

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
especificar o `pluginname`. Neste momento não vou me preocupar com o idioma,
então escreverei em português mesmo estando na pasta `en`. No mundo real,
você criaria `local/tudoupper/lang/pt_br/local_tudoupper.php` 
e `local/tudoupper/lang/en/local_tudoupper.php` e colocaria as strings
correspondentes de cada língua.

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

### Composer

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

### Api de configuração

A [página](https://docs.moodle.org/dev/Admin_settings) contém bastante informações
sobre a API de configuração.

Vamos criar uma nova entrada em `lang/en/local_tudoupper.php`:
{% highlight php %}
<?php
defined('MOODLE_INTERNAL') || die();
$string['pluginname'] = 'Plugin que deixa tudo maiúsculo';
$string['title'] = 'Configurações do plugin super massa tudoupper';
{% endhighlight %}

Adicionemos um novo arquivo chamado `settings.php` no nosso plugin
tendo uma condição com `$hassiteconfig` que restringe esse acesso 
apenas para administradores da plataforma. 
Manipularemos um objetos do tipo `admin_settingpage` que cuidará 
da camada de formulário e persistência no banco de dados das
configurações do plugin. Depois adicionamos esse objeto na variável global 
`$ADMIN` que se encarregará de disponibilizar as opções do nosso
plugin na área de configurações da plataforma. 

{% highlight php %}
<?php
defined('MOODLE_INTERNAL') || die();
 
if ($hassiteconfig) {
    $title = new lang_string('title', 'local_tudoupper');
    $settings = new admin_settingpage('local_tudoupper', $title);
    $ADMIN->add('localplugins', $settings);
}
{% endhighlight %}

Suba a versão em `version.php` e agora em `Site Administration` -> 
`Plugins` -> `Local Plugins` temos uma entrada para configuração do
nosso plugin, ainda sem campo algum. 

Vamos adicionar os seguintes campos, em parentese estão as classes moodle
da api de formulário que fornece o markup necessário para cada tipo:

- checkbox: ativar ou desativa o recurso desse plugin (admin_setting_configcheckbox)
- select: para usar tudo em uppercase ou camelCase (admin_setting_configselect)
- input text: prefixo (admin_setting_configtext)
- input text: suffixo (admin_setting_configtext)

Começamos complementando nossas strings em `lang/en/local_tudoupper.php`:
{% highlight php %}
<?php
defined('MOODLE_INTERNAL') || die();

$string['pluginname'] = 'Plugin que deixa tudo maiúsculo';
$string['title'] = 'Configurações do plugin super massa tudoupper';

$string['enabled'] = 'Habilitar tudoupper?';
$string['enabled_description'] = 'Habilitar esse recurso na plataforma moodle';

$string['type'] = 'Configura tipo';
$string['type_description'] = 'Tipo que deseja para o plugin tudoupper';
$string['type_upper'] = 'Tudo em Maiúscula';
$string['type_camelcase'] = 'Tudo em CamelCase';

$string['prefix'] = 'Configura prefixo';
$string['prefix_description'] = 'Colocar um prefixo em todas strings';

$string['suffix'] = 'Configura sufixo';
$string['suffix_description'] = 'Colocar um sufixo em todas strings';

{% endhighlight %}

Inicialmente vamos adicionar somente o campo `$enabled`:

{% highlight php %}
<?php
defined('MOODLE_INTERNAL') || die();
 
if ($hassiteconfig) {
    
    # Inicializando objeto admin_settingpage
    $title = new lang_string('title', 'local_tudoupper');
    $settings = new admin_settingpage('local_tudoupper', $title);

    # Campo para habilitar ou desabilitar recurso
    $enabled = new lang_string('enabled', 'local_tudoupper');
    $enabled_description = new lang_string('enabled_description', 'local_tudoupper');
    $field_enabled = new admin_setting_configcheckbox('local_tudoupper/enabled',$enabled,$enabled_description,1);

    # Adicionado campos na área de configuração
    $settings->add($field_enabled);
    $ADMIN->add('localplugins', $settings);
}
{% endhighlight %}

Antes de adicionarmos os demais campos, vamos ler essa opção na nossa
classe `tudoupper_string_manager` e habilitar ou não o recurso:

{% highlight php %}
<?php
namespace local_tudoupper;

defined('MOODLE_INTERNAL') || die();
require_once($CFG->dirroot . '/local/tudoupper/vendor/autoload.php');

use Jawira\CaseConverter\Convert;

class tudoupper_string_manager extends \core_string_manager_standard {
  public function get_string($identifier, $component = '', $a = null, $lang = null) {

    $string = parent::get_string($identifier, $component, $a , $lang );

    # só prosseguimos se o recurso estiver habilitado
    $enabled = get_config('local_tudoupper','enabled');
    if(!$enabled) return $string;
    
    $obj = new Convert($string);
    return $obj->toCamel();
  }
}
{% endhighlight %}

Agora pela interface de configuração podemos desativar ou ativar esse recurso.

Adicionemos os demais campos:

{% highlight php %}
<?php
defined('MOODLE_INTERNAL') || die();
 
if ($hassiteconfig) {
    
    # Inicializando objeto admin_settingpage
    $title = new lang_string('title', 'local_tudoupper');
    $settings = new admin_settingpage('local_tudoupper', $title);

    # Campo para habilitar ou desabilitar recurso
    $enabled = new lang_string('enabled', 'local_tudoupper');
    $enabled_description = new lang_string('enabled_description', 'local_tudoupper');
    $field_enabled = new admin_setting_configcheckbox('local_tudoupper/enabled',$enabled,$enabled_description,1);

    # Campos tipo
    $type = new lang_string('type', 'local_tudoupper');
    $type_description = new lang_string('type_description', 'local_tudoupper');
    $type_upper = new lang_string('type_upper', 'local_tudoupper');
    $type_camelcase = new lang_string('type_camelcase', 'local_tudoupper');
    $default = 'upper';
    $options = ['upper' => $type_upper, 'camelcase' => $type_camelcase];
    $field_type = new admin_setting_configselect('local_tudoupper/type',$type, $type_description, $default, $options);

    # Campo prefixo
    $prefix = new lang_string('prefix', 'local_tudoupper');
    $prefix_description = new lang_string('prefix_description', 'local_tudoupper');
    $default = '';
    $field_prefix = new admin_setting_configtext('local_tudoupper/prefix',$prefix,$prefix_description,$default);

    # Campo prefixo
    $suffix = new lang_string('suffix', 'local_tudoupper');
    $suffix_description = new lang_string('suffix_description', 'local_tudoupper');
    $default = '';
    $field_suffix = new admin_setting_configtext('local_tudoupper/suffix',$suffix,$suffix_description,$default);

    # Adicionado campos na área de configuração
    $settings->add($field_enabled);
    $settings->add($field_type);
    $settings->add($field_prefix);
    $settings->add($field_suffix);
    $ADMIN->add('localplugins', $settings);
}
{% endhighlight %}

Por fim modificaremos a classe `tudoupper_string_manager` para usar
esses novos campos:
{% highlight php %}
<?php
namespace local_tudoupper;

defined('MOODLE_INTERNAL') || die();
require_once($CFG->dirroot . '/local/tudoupper/vendor/autoload.php');

use Jawira\CaseConverter\Convert;

class tudoupper_string_manager extends \core_string_manager_standard {
  public function get_string($identifier, $component = '', $a = null, $lang = null) {

    $string = parent::get_string($identifier, $component, $a , $lang );

    # só prosseguimos se o recurso estiver habilitado
    $enabled = get_config('local_tudoupper','enabled');
    if(!$enabled) return $string;

    # prefixo e sufixo das strings
    $prefix = get_config('local_tudoupper','prefix');
    $suffix = get_config('local_tudoupper','suffix');
    $string =  $prefix . $string .  $suffix;

    # tipo
    $type = get_config('local_tudoupper','type');
    if($type == 'upper') return strtoupper($string);
    if($type == 'camelcase') {
      $obj = new Convert($string);
      return $obj->toCamel();
    }
    return $string;
  }
}
{% endhighlight %}





