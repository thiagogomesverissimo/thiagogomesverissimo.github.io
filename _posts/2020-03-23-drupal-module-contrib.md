---
title: 'Desenvolvendo módulos para Drupal'
date: 2020-03-23
permalink: /posts/drupal-modules
categories:
  - tutorial
tags:
  - drupal
---

Coleção de dicas e Drupal para desenvover módulos para Drupal, nada que
substitua a documentação oficial

# Instalação básica de uma instância para desenvolvimento (Debian 10)

Pacotes básicos para instalar o Drupal no seu debian usando sqlite3:

{% highlight bash %}
apt-get install php php-common php-cli php-gd php-curl php-xml php-mbstring php-sqlite3 sqlite3
{% endhighlight %}

Instalação do composer globalmente:
{% highlight bash %}
curl -s https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer
{% endhighlight %}

Criando uma instalação limpa para começar a desenvolver. Será criado um
diretório chamado projetodev, sendo usuário/senha igual a admin/admin:

{% highlight bash %}
composer create-project drupal-composer/drupal-project:8.x-dev projetodev --no-interaction
cd projetodev
./vendor/bin/drupal site:install standard --db-type="sqlite" \
       --site-name="Ambiente Dev" --site-mail="dev@locahost" \
       --account-name="admin" --account-pass="admin" --account-mail="dev@localhost" \
       --no-interaction
{% endhighlight %}

Subindo um server local para desenvolvimento:

{% highlight bash %}
./vendor/bin/drupal serve -v
{% endhighlight %}

Caso precise zerar o banco e começar tudo novamente:
{% highlight bash %}
rm web/sites/default/files/.ht.sqlite*
{% endhighlight %}

Desligando o cache durante o desenvolvimento:
{% highlight bash %}
./vendor/bin/drupal site:mode dev
{% endhighlight %}

Religando o cache:
{% highlight bash %}
./vendor/bin/drupal site:mode prod
{% endhighlight %}

./vendor/bin/drupal site:mode dev

# Dicas para configurar seu ambiente

Alias para colocar no seu bashrc:

{% highlight bash %}
alias drupalcs="phpcs --standard=Drupal --extensions='php,module,inc,install,test,profile,theme,css,info,txt,md'" 
alias drupalcsp="phpcs --standard=DrupalPractice --extensions='php,module,inc,install,test,profile,theme,css,info,txt,md'" 
alias drupalcbf="phpcbf --standard=Drupal --extensions='php,module,inc,install,test,profile,theme,css,info,txt,md'"
{% endhighlight %}

Usando pareviewsh localmente (mesmo efeito de usar
pelo site https://pareview.sh/):

{% highlight bash %}
mkdir ~/temp
cd temp
git clone https://git.drupalcode.org/project/pareviewsh
cd pareviewsh
composer install
{% endhighlight %}

# Estrutura de um módulo

## rotas
Exemplo de entrada no arquivo *exemplo.routing.yml*:
{% highlight bash %}
exemplo.bla:
  path: '/bla'
  defaults:
    _controller: '\Drupal\exemplo\Controller\ExemploController::bla'
  requirements:
    _permission: 'access content'
{% endhighlight %}

Rota que injeta a variável $parametro no médoto bla: 
*bla($parametro)* do classe ExemploController:
{% highlight bash %}
exemplo.bla:
  path: '/bla/{parametro}'
  defaults:
    _controller: '\Drupal\exemplo\Controller\ExemploController::bla'
  requirements:
    _permission: 'access content'
{% endhighlight %}

Rota que injeta a variável $parametro agora como o um objeto node,
isto é, {parametro} agora será o id no node. E teremos de "graça"
o objeto node relacionado ao id passado no nosso método bla():
{% highlight bash %}
exemplo.bla:
  path: '/bla/{parametro}'
  defaults:
    _controller: '\Drupal\exemplo\Controller\ExemploController::bla'
  requirements:
    _permission: 'access content'
  options:
    parameters:
      parametro:
        type: entity:node
{% endhighlight %}

## controller
Controller básico:
{% highlight bash %}
...
use Drupal\Core\Controller\ControllerBase;

class ExemploController extends ControllerBase{
  public function hello(){
    return [
      '#markup' => $this->t('Hello People')
    ];
  }
}
{% endhighlight %}

## Carregando configurações dentro de um service

Suponha que sua classe src/Service/Uteis.php precise
carregar configurações do site.

Na declaração de *exemplo.services.yml*:
{% highlight bash %}
services:
  exemplo.uteis:
    class: Drupal\exemplo\Service\Uteis
    arguments: ['@config.factory']
{% endhighlight %}

Em src/Service/Uteis.php declare:
{% highlight bash %}
use Drupal\Core\Config\ConfigFactoryInterface;
{% endhighlight %}

E por fim, injete $config_factory no __construct:
{% highlight bash %}
protected $config_factory;
public function __construct(ConfigFactoryInterface $config_factory){
  $this->config_factory = $config_factory;
}
{% endhighlight %}

Agora é possível carregar configurações em qualquer métodos
de Uteis.php assim:
{% highlight bash %}
$this->config_factory->get('NOME_DA_CONFIG');
{% endhighlight %}

## Receita para injetar um serviço no controller

Primeiro sua classe deve existir, por exemplo src/Service/Uteis,
e ser declarada em *exemplo.services.yml*:
{% highlight bash %}
services:
  exemplo.inverte:
    class: Drupal\exemplo\Service\Uteis
{% endhighlight %}

No seu controller declarar *ContainerInterface* e sua classe:
{% highlight bash %}
<?
...
use Symfony\Component\DependencyInjection\ContainerInterface;
use Drupal\exemplo\Service\Uteis;
{% endhighlight %}

No __construct do controller receber a classe como paramêtro numa variável
local:
{% highlight bash %}
protected $uteis;
public function __construct(Uteis $uteis){
  $this->uteis = $uteis;
}
{% endhighlight %}

Por fim, no método create(), que é chamado antes do controller:
{% highlight bash %}
public static function create(ContainerInterface $container){
  return new static (
    $container->get('exemplo.uteis')
  );
}
{% endhighlight %}
Sua variável *$this->uteis* está pronta para uso.
Sempre olhar o __contruct() e create() da classe pai da qual 
esteja injetando o service, pois neste caso, você deve injetar os
services que a classe pai também injeta.

## Formulário de configuração do módulo

Criar rota que aponta par ao Form
{% highlight bash %}
exemplo.configuracoes:
  path: '/admin/config/exemplo'
  defaults:
    _form: '\Drupal\exemplo\Form\ConfiguracoesForm'
  requirements:
    _permission: 'administer site configuration'
{% endhighlight %}

Criar a classe do formulário em src/Form 
extendendo ConfigFormBase:

{% highlight bash %}
<?php

namespace Drupal\exemplo\Form;

use Drupal\Core\Form\ConfigFormBase;
use Drupal\Core\Form\FormStateInterface;

class ConfiguracoesForm extends ConfigFormBase {

  public function getFormId() {
    return 'exemplo_admin_settings';
  }

  protected function getEditableConfigNames() {
    return [
      'exemplo.settings',
    ];
  }

  public function buildForm(array $form, FormStateInterface $form_state) {
    $config = $this->config('exemplo.settings');
    $form['um_texto_qualquer'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Digite um texto qualquer'),
      '#default_value' => $config->get('um_texto_qualquer'),
    ];
    return parent::buildForm($form, $form_state);
  }

  public function validateForm(array &$form, FormStateInterface $form_state) {
    $x = $form_state->getValue('um_texto_qualquer');
    if($x == 'José'){
      $form_state->setErrorByName('um_texto_qualquer',$this->t('José não vai...'));
    }
  }

  public function submitForm(array &$form, FormStateInterface $form_state) {
    $this->config('exemplo.settings')
      ->set('um_texto_qualquer', $form_state->getValue('um_texto_qualquer'))
      ->save();
    parent::submitForm($form, $form_state);
  }

}
{% endhighlight %}

Não precisamos necessariamente apontar uma rota para o nosso
formulário. Podemos redenderizar o formulário do controller assim, 
injetando o serviço *form_builder*:


{% highlight bash %}
...
use Symfony\Component\DependencyInjection\ContainerInterface;
use Drupal\Core\Form\FormBuilder;
...
  protected $builder;
  public function __construct(Uteis $uteis, FormBuilder $builder){
    $this->uteis = $uteis;
    $this->builder = $builder;
  }
  public static function create(ContainerInterface $container){
    return new static(
      $container->get('form_builder')
    );

  /*No seu método pode carrgar o form: */
  $form = $this->builder->getForm('Drupal\tofu\Form\ConfiguracoesForm');
  return $form;
{% endhighlight %}
A vantagem nesse caso é que a variável *$form* é um render array
que pode ser manipulado.

## alter form - exemplo: modificando a página de informações do site

Primeiramente, vamos descobrir a rota do formulário:

{% highlight bash %}
./vendor/bin/drupal debug:router| grep site-information
{% endhighlight %}

Agora que sabemos a rota, vamos descobrir qual é o formulário:
{% highlight bash %}
/vendor/bin/drupal debug:router system.site_information_settings
{% endhighlight %}

Sabendo que o formulário está em *core/modules/system/src/Form/SiteInformationForm.php* 
identificamos o id retornado no método getFormId(): *system_site_information_settings *

Em exemplo.module podemos implementar o hook_form_ID_alter.
Vamos colocar um campo de texto a mais na página de configuração, validar
e salvar:
{% highlight bash %}
function exemplo_form_system_site_information_settings_alter(&$form, \Drupal\Core\Form\FormStateInterface $form_state, $form_id){
    $config = \Drupal::service('config.factory')->getEditable('system.site');
    $form['um_texto_qualquer'] = [
      '#type' => 'textfield',
      '#title' => 'Digite um texto qualquer',
      '#default_value' => $config->get('um_texto_qualquer'),
    ];
    /* Métodos para salvar e validar novo campo*/
    $form['#submit'][] = '_um_texto_qualquer_form_submit';
    $form['#validate'][] = '_um_texto_qualquer_form_validate';
}

function _um_texto_qualquer_form_submit(&$form, \Drupal\Core\Form\FormStateInterface $form_state){
    $config = \Drupal::service('config.factory')->getEditable('system.site');
    $config->set('um_texto_qualquer',$form_state->getValue('um_texto_qualquer'))->save();
}

function _um_texto_qualquer_form_validate(&$form, \Drupal\Core\Form\FormStateInterface $form_state){

    $x = $form_state->getValue('um_texto_qualquer');
    if($x == 'José'){
      $form_state->setErrorByName('um_texto_qualquer','José não, vai...');
    }
}
{% endhighlight %}

Elementos que podemos colocar no formulário:
[https://api.drupal.org/api/drupal/elements/8.9.x](https://api.drupal.org/api/drupal/elements/8.9.x)

# Links importantes:

 - [Padrões de escrita de códigos](https://www.drupal.org/docs/develop/documenting-your-project/help-text-standards)
 - [Instalação global do codesniffer](https://www.drupal.org/docs/8/modules/code-review-module/installing-coder-sniffer)
 - [Usando codesniffer por linha de comando](https://www.drupal.org/docs/8/modules/code-review-module/php-codesniffer-command-line-usage)


