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
substitua a documentação oficial. 

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
Todos exemplos serão baseados em um módulo fictício chamado *tofu*.

## Exemplos com declarações de rotas
Exemplo de entrada da rota */bla* no arquivo *tofu.routing.yml*
que aponta para o método *bla* da classe ExemploController:

{% highlight bash %}
tofu.bla:
  path: '/bla'
  defaults:
    _controller: '\Drupal\tofu\Controller\ExemploController::bla'
  requirements:
    _permission: 'access content'
{% endhighlight %}

Para recebermos no médoto *bla* um parâmetro, *bla($parametro)*, 
recebido como segundo argumento na rota:
{% highlight bash %}
tofu.bla:
  path: '/bla/{parametro}'
  defaults:
    _controller: '\Drupal\tofu\Controller\ExemploController::bla'
  requirements:
    _permission: 'access content'
{% endhighlight %}

Rota que injeta a variável $parametro agora como o um objeto node,
isto é, {parametro} agora será o id no node. E teremos de "graça"
o objeto node relacionado ao id passado no nosso método *bla*:
{% highlight bash %}
tofu.bla:
  path: '/bla/{parametro}'
  defaults:
    _controller: '\Drupal\tofu\Controller\ExemploController::bla'
  requirements:
    _permission: 'access content'
  options:
    parameters:
      parametro:
        type: entity:node
{% endhighlight %}

## Exemplos com Controllers

Controller básico estende ControllerBase:
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

## Injetando service *config.factory* em classes do seu sistema

Suponha que sua classe src/Service/Uteis.php precise
carregar configurações do site.

Na declaração de *tofu.services.yml*:
{% highlight bash %}
services:
  tofu.uteis:
    class: Drupal\tofu\Service\Uteis
    arguments: ['@config.factory']
{% endhighlight %}

Em src/Service/Uteis.php declare ConfigFactoryInterface:
{% highlight bash %}
use Drupal\Core\Config\ConfigFactoryInterface;
{% endhighlight %}

E por fim, injete *$config_factory* no __construct:
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

Primeiro sua classe deve existir, por exemplo src/Service/Uteis.
Vamos definir essa classe como um Service em *tofu.services.yml*:
{% highlight bash %}
services:
  tofu.inverte:
    class: Drupal\tofu\Service\Uteis
{% endhighlight %}

Para usar essa classe no controller, mas carregada como serviço, 
fazemos os seguintes passos:

1 - No seu controller declarar *ContainerInterface* e sua classe (aquela
que transformamos em service):
{% highlight bash %}
<?
...
use Symfony\Component\DependencyInjection\ContainerInterface;
use Drupal\tofu\Service\Uteis;
{% endhighlight %}

2 - No __construct do controller receber a classe como paramêtro em 
uma variável local:
{% highlight bash %}
protected $uteis;
public function __construct(Uteis $uteis){
  $this->uteis = $uteis;
}
{% endhighlight %}

3 - Por fim, no método create(), que é chamado antes do controller,
carregar o $container com os serviço *uteis*:
{% highlight bash %}
public static function create(ContainerInterface $container){
  return new static (
    $container->get('tofu.uteis')
  );
}
{% endhighlight %}

Agora, sua variável *$this->uteis* está pronta para uso em
qualquer lugar do controller.

Sempre olhar o __contruct() e create() da classe mãe da qual 
esteja injetando o service, pois neste caso, você deve injetar os
services que a classe mãe também injeta. Assim, supondo que
sua classe mãe injete mais dois serviços, $a e $b, para injetar
o nosso *tofu.uteis* faríamos no controller:
{% highlight bash %}
protected $uteis;
public function __construct(A $a, B $b, Uteis $uteis,){
  parent::__construct($a, $b);
  $this->uteis = $uteis;
}
{% endhighlight %}

E no método create retornamos todos serviços que já eram carregados
mais o nosso:
{% highlight bash %}
public static function create(ContainerInterface $container){
  return new static (
    $container->get('modulo1.a'),
    $container->get('modulo2.b'),
    $container->get('tofu.uteis')
  );
}
{% endhighlight %}

## Formulário de configuração do módulo

A seguir estão os passos para criamos um formulário de
configuração de um módulo, delegando para o sistema de configuração,
o armazenamento dos dados.

1 - Criando rota que aponta para ao classe do tipo Form:
{% highlight bash %}
tofu.configuracoes:
  path: '/admin/config/tofu'
  defaults:
    _form: '\Drupal\tofu\Form\ConfiguracoesForm'
  requirements:
    _permission: 'administer site configuration'
{% endhighlight %}

2 - Se quiser uma entrada na área de configurações
do site para esse módulo, em tofu.links.menu.yml
inserir seguinte conteúdo:
{% highlight bash %}
tofu.configuracoes:
  title: 'Módulo Tofu'
  route_name: tofu.configuracoes
  description: 'Configurações do módulo tofu'
  parent: system.admin_config_system
  weight: 99
{% endhighlight %}

3 - Criar a classe do formulário em src/Form estendendo ConfigFormBase,
olhe cada método, eles são bem intuitivos. O formulário é construído no
*buildForm*, veja uma lista de tipos de campos possíveis em 
[https://api.drupal.org/api/drupal/elements](https://api.drupal.org/api/drupal/elements).
Em validateForm, adivinhe, validamos o formulário. 
Em submitForm salvamos, mas podemos processar os valores antes de salvar.
E em getEditableConfigNames carregamos o serviço de configuração.
{% highligh bash %}
<?php

namespace Drupal\tofu\Form;

use Drupal\Core\Form\ConfigFormBase;
use Drupal\Core\Form\FormStateInterface;

class ConfiguracoesForm extends ConfigFormBase {

  public function getFormId() {
    return 'tofu_admin_settings';
  }

  protected function getEditableConfigNames() {
    return [
      'tofu.settings',
    ];
  }

  public function buildForm(array $form, FormStateInterface $form_state) {
    $config = $this->config('tofu.settings');
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
    $this->config('tofu.settings')
      ->set('um_texto_qualquer', $form_state->getValue('um_texto_qualquer'))
      ->save();
    parent::submitForm($form, $form_state);
  }

}
{% endhighlight %}

Não precisamos necessariamente apontar uma rota para o nosso
formulário. Podemos redenderizar o formulário de dentro do controller
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

  ...
  // No seu método pode carregar o form:
  $form = $this->builder->getForm('Drupal\tofu\Form\ConfiguracoesForm');
  return $form;
  ...
{% endhighlight %}

A vantagem nesse caso é que a variável *$form* é um render array
que pode ser manipulado antes de ser retornado.

## alter ID form: exemplo modificando a página de informações do site

Temos que saber o ID do formulário, aquele definido em getFormId(). 
Um caminho é identificar a rota do formulário:
{% highlight bash %}
./vendor/bin/drupal debug:router| grep site-information
{% endhighlight %}

E sabendo-se a rota, podemos ver qual é a classe do formulário:
{% highlight bash %}
/vendor/bin/drupal debug:router system.site_information_settings
{% endhighlight %}

Encontramos assim que o formulário está em 
*core/modules/system/src/Form/SiteInformationForm.php* 
identificamos o id retornado no método getFormId(): *system_site_information_settings*.

Em *tofu.module* podemos implementar o hook_form_ID_alter.
No nosso exemplo, vamos:
colocar um campo de texto a mais na página de configuração, validar e salvar:
{% highlight bash %}
function tofu_form_system_site_information_settings_alter(&$form, \Drupal\Core\Form\FormStateInterface $form_state, $form_id){
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

## Plugin: Bloco customizado

Vamos criar um plugin e esse plugin será um bloco customizado dentro
de src/Plugin/Block.

1 - Criar classe TofuBlock (src/Plugin/Block/TofuBlock.php) estendendo
BlockBase. Basta criarmos uma annotation com o id e título do bloclo.
O único método que precisamos é o build() que deve retornar um render 
array com o markup do texto que será mostrado no bloco.

{% highlight bash %}
namespace Drupal\tofu\Plugin\Block;
use Drupal\Core\Block\BlockBase;

/**
 * @Block(
 *   id = "tofu_block",
 *   admin_label = @Translation("Bloco do Tofu"),
 * )
 */
class TofuBlock extends BlockBase {
  public function build() {
    return [
      '#markup' => $this->t('Sou o bloco tofu'),
    ];
  }
}
{% endhighlight %}

Mas e se queremos manipular configurações dentro do nosso bloco?
Neste caso, ao invés de injetar o config.factory, vamos implementar uma interface. 
Se for apenas configuração que precisamos injetar o mais fácil é implementar 
BlockPluginInterface, e usar a configuração relacionada ao bloco com
*$this->getConfiguration()*. Vamos aproveitar e implementar o método
blockForm para mostrar um formulário na configuração do bloco, com apenas um campo,
e blockSubmit para salvar a configuração e blockValidate para validar os campos.

{% highlight bash %}
namespace Drupal\tofu\Plugin\Block;

use Drupal\Core\Block\BlockBase;
use Drupal\Core\Block\BlockPluginInterface;
use Drupal\Core\Form\FormStateInterface;

/**
 * @Block(
 *   id = "tofu_block",
 *   admin_label = @Translation("Bloco do Tofu"),
 * )
 */
class TofuBlock extends BlockBase implements BlockPluginInterface {

  public function build() {
    $config = $this->getConfiguration();
    $nome = isset($config['nome']) ? $config['nome'] : 'sem nome...';
    return [
      '#markup' => $this->t('Sou o bloco tofu. Meu nome é: @nome',[
        '@nome' => $nome
      ]),
    ];  
  }
  public function blockForm($form, FormStateInterface $form_state) {
    $form = parent::blockForm($form, $form_state);
    $config = $this->getConfiguration();

    $form['nome'] = array(
      '#type' => 'textfield',
      '#title' => t('Nome'),
      '#default_value' => isset($config['nome']) ? $config['nome'] : 'Sem nome...',
    );
    return $form;
  }

  public function blockSubmit($form, FormStateInterface $form_state) {
    $this->setConfigurationValue('nome', $form_state->getValue('nome'));
  }

  public function blockValidate($form, FormStateInterface $form_state) {
    $nome = $form_state->getValue('nome');

    if ($nome != 'Tofu') {
      $form_state->setErrorByName('nome', t('Esse nome não é bonito!'));
    }
  }
}
{% endhighlight %}

Tudo muito bonito. Mas e se precisarmos injetar outro serviço que não a 
configuração? Por exemplo, o *tofu.uteis*?
Neste caso o melhor é implementar ContainerFactoryPluginInterface, o que nos
obriga a declarar __construct e create(), levemente diferente dos que que já vimos
até agora, pois estamos no contexto do plugin, e temos que passar o id e definition 
do mesmo. O interessante é que ganhamos de graça o array de configuração $config,
então eu particularmente prefiro implementar ContainerFactoryPluginInterface 
do que BlockPluginInterface. 

{% highlight bash %}
namespace Drupal\tofu\Plugin\Block;

use Drupal\Core\Block\BlockBase;
use Drupal\Core\Plugin\ContainerFactoryPluginInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;
use Drupal\tofu\Service\Uteis;

/**
 * @Block(
 *   id = "tofu_block",
 *   admin_label = @Translation("Bloco do Tofu"),
 * )
 */
class TofuBlock extends BlockBase implements ContainerFactoryPluginInterface {

  protected $uteis;
  public function __construct(array $config, 
    $plugin_id, $plugin_definition, Uteis $uteis){
    parent::__construct($config, $plugin_id, $plugin_definition);
    $this->uteis = $uteis;
  }

  public static function create(ContainerInterface $container, 
    array $config, $plugin_id, $plugin_definition){
    return new static (
      $config,
      $plugin_id, 
      $plugin_definition,
      $container->get('tofu.uteis')
    );
  }

  public function build() { 
    return [
      '#markup' => $this->t($this->uteis->inverte(" M A R I A ")),
    ];
  }
}
{% endhighlight %}
