---
title: 'Tópicos em desenvolvimento de módulos para Drupal'
date: 2020-03-23
permalink: /posts/drupal-modules
categories:
  - tutorial
tags:
  - drupal
---

Coleção de dicas para desenvover módulos para Drupal, nada que
substitua a documentação oficial.

<ul id="toc"></ul>

## Criando uma instância Drupal para desenvolvimento com Debian 10

Pacotes básicos para subirmos uma instância de drupal com sqlite3 no debian 10:

{% highlight bash %}
apt-get install php php-common php-cli php-gd php-curl php-xml php-mbstring php-sqlite3 sqlite3
{% endhighlight %}

Instalação do composer globalmente:
{% highlight bash %}
curl -s https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer
{% endhighlight %}

Criando uma instalação limpa para começar a desenvolver. Será criado um
diretório chamado drupal-dev, sendo usuário/senha igual a admin/admin:

{% highlight bash %}
composer create-project drupal/recommended-project:8.x drupal-dev
cd drupal-dev
composer require drupal/console
composer require drush/drush:8.x
./vendor/bin/drush site-install standard \
  --db-url=sqlite://sites/default/files/.ht.sqlite \
  --site-name="Ambiente Dev" \
  --site-mail="dev@locahost" \
  --account-name="admin" \
  --account-pass="admin" \
  --account-mail="dev@localhost" --yes
{% endhighlight %}

Normalmente, eu ignoro as pastas *vendor*, *web* e *drush* no gitignore.

Subindo um server local para desenvolvimento:

{% highlight bash %}
./vendor/bin/drupal serve -v
{% endhighlight %}

Caso precise zerar o banco e começar tudo novamente:
{% highlight bash %}
rm web/sites/default/files/.ht.sqlite*
{% endhighlight %}

## Criando um módulo 

Todos exemplos serão baseados em um módulo fictício chamado *tofu*.
Para o drupal reconhecer nosso módulo, isto é, o mesmo aparecer na 
lista de módulos para serem habilitados, necessitamos criar uma pasta chamada
*tofu* com o arquivo *tofu.info.yml*, o qual contém informações básicas do módulo.
O comando abaixo se encarrega de criar o módulo *tofu*:

{% highlight bash %}
./vendor/bin/drupal generate:module  \
  --module="tofu"  \
  --machine-name="tofu"  \
  --module-path="modules"  \
  --description="Módulo Tofu"  \
  --core="8.x"  \
  --no-interaction
{% endhighlight %}

## Rotas

### Criando rota e controller 
As entradas de rotas são definidas em *tofu.routing.yml*.
O comando a seguir vai gerar o controller TofuController com um método
chamado *index()*, assim como uma rota */tofu* apontando para esse método:

{% highlight bash %}
./vendor/bin/drupal generate:controller  \
  --module="tofu"  \
  --class="TofuController"  \
  --routes='"title":"index", "name":"tofu.index", "method":"index", "path":"/tofu"'  \
  --no-interaction
{% endhighlight %}

A entrada criada em *tofu.routing.yml* tem a forma:
{% highlight yaml %}
tofu.index:
  path: '/index'
  defaults:
    _controller: '\Drupal\tofu\Controller\TofuController::index'
  requirements:
    _permission: 'access content'
{% endhighlight %}

### Rota com parâmetros

Se no método *index()* do controller quisermos receber um parâmetro,
por exemplo, *index($parametro)*, modificaríamos nosso arquivo de rota assim:

{% highlight yaml %}
tofu.index:
  path: '/index/{parametro}'
  defaults:
    _controller: '\Drupal\tofu\Controller\TofuController::index'
  requirements:
    _permission: 'access content'
{% endhighlight %}

### Carregando node automaticamente a partir do nid na rota

O Drupal vai muito além. Suponha que esse $parametro,
por algum motivo, seja o *nid* de nodes do seu site. 
Poderíamos, dentro do controller, carregar o node baseado nos id recebido,
mas podemos fazer essa injeção diretamente no arquivo de rotas, assim,
a variável $parametro será diretamente um objeto do tipo node:
{% highlight yaml %}
tofu.index:
  path: '/bla/{parametro}'
  defaults:
    _controller: '\Drupal\tofu\Controller\TofuController::index'
  requirements:
    _permission: 'access content'
  options:
    parameters:
      parametro:
        type: entity:node
{% endhighlight %}

## Controllers

Exemplo básico de um controller:
{% highlight php %}
use Drupal\Core\Controller\ControllerBase;

class ExemploController extends ControllerBase{
  public function index(){
    return [
      '#markup' => $this->t('Hello People')
    ];
  }
}
{% endhighlight %}

## Services

### Criando e utilizando services

Vamos criar a classe *UteisService.php* e veremos como utilizá-la no controller.
 
{% highlight bash %}
./vendor/bin/drupal generate:service  \
  --module="tofu"  \
  --name="tofu.uteis"  \
  --class="UteisService"  \
  --path-service="src" \
  --no-interaction
{% endhighlight %}

Note que foi criada uma entrada em *tofu.services.yml* que define nossa classe como
um serviço para o drupal.

Na classe *UteisService.php*, como exemplo, vamos criar um método que dada uma string,
a devolve invertida e com todas letras em maisculá:

{% highlight php %}
public function inverte($string){
  return strtoupper(strrev($string));
}
{% endhighlight %}

### Injetando um serviço no controller

Queremos usar no nosso controller o método *inverte($string)* que está em *UteisService.php*, mas carregado como serviço. Isso significa que ao chamarmos
*$this->tofuUteis->inverte('Maria')* recebemos como resposta *AIRAM*.

Usando o mesmo comando do drupal console para criar a rota */tofu* e o controller *TofuControler* podemos passar a flag services e especificar o serviço *tofu.uteis*:
{% highlight php %}
./vendor/bin/drupal generate:controller  \
  --module="tofu"  \
  --class="TofuController"  \
  --routes='"title":"index", "name":"tofu.index", "method":"index", "path":"/tofu"'  \
  --services="tofu.uteis" \
  --no-interaction
{% endhighlight %}

A saída será como abaixo, criando uma váriável *$tofuUteis*, objeto instanciado
do nosso serviço.
{% highlight php %}
  use Symfony\Component\DependencyInjection\ContainerInterface;
  ...
  protected $tofuUteis;
  public static function create(ContainerInterface $container) {
    $instance = parent::create($container);
    $instance->tofuUteis = $container->get('tofu.uteis');
    return $instance;
  }
{% endhighlight %}

Eu costumo também fazer de outra maneira, não sei qual é a melhor forma de injetar
o serviço no controller, mas ambas funcionam. Forma manual:

1 - No controller, declarar *ContainerInterface* e a classe do serviço:
{% highlight php %}
use Symfony\Component\DependencyInjection\ContainerInterface;
use Drupal\tofu\UteisService;
{% endhighlight %}

2 - No __construct do controller receber a classe do serviço 
como paramêtro em atribuir numa variável local:
{% highlight php %}
protected $tofuUteis;
public function __construct(UteisService $tofuUteis){
  $this->tofuUteis = $tofuUteis;
}
{% endhighlight %}

3 - Por fim, no método create(), que é chamado antes do controller,
carregar o $container com o serviço:
{% highlight php %}
public static function create(ContainerInterface $container){
  return new static (
    $container->get('tofu.uteis')
  );
}
{% endhighlight %}

Sempre olhar o __contruct() e create() da classe mãe da qual 
esteja injetando o service, pois neste caso, você deve injetar os
services que a classe mãe também injeta. Assim, supondo que
sua classe mãe injete mais dois serviços, $a e $b, para injetar
o nosso *tofu.uteis* faríamos assimo no controller:

{% highlight php %}
protected $tofuUteis;
public function __construct(A $a, B $b, UteisService $tofuUteis){
  parent::__construct($a, $b);
  $this->tofuUteis = $tofuUteis;
}
{% endhighlight %}

E no método create retornamos todos serviços que já eram carregados,
acrescentando o nosso:
{% highlight php %}
public static function create(ContainerInterface $container){
  return new static (
    $container->get('modulo1.a'),
    $container->get('modulo2.b'),
    $container->get('tofu.uteis')
  );
}
{% endhighlight %}

DAQUI PARA BAIXO FALTA REVISAR
-----------------------------------------------------------------------------

### Injetando service *config.factory* em classes do seu sistema

Suponha que sua classe src/Service/Uteis.php precise
carregar configurações do site.


{% highlight bash %}
./vendor/bin/drupal generate:service  \
--module="tofu"  \
--name="tofu.uteis"  \
--class="UteisService"  \
--path-service="src/Service" \
--services="config.factory" \
  --no-interaction
{% endhighlight %}


Na declaração de *tofu.services.yml*:
{% highlight php %}
services:
  tofu.uteis:
    class: Drupal\tofu\Service\Uteis
    arguments: ['@config.factory']
{% endhighlight %}

Em src/Service/Uteis.php declare ConfigFactoryInterface:
{% highlight php %}
use Drupal\Core\Config\ConfigFactoryInterface;
{% endhighlight %}

E por fim, injete *$config_factory* no __construct:
{% highlight php %}
protected $config_factory;
public function __construct(ConfigFactoryInterface $config_factory){
  $this->config_factory = $config_factory;
}
{% endhighlight %}

Agora é possível carregar configurações em qualquer métodos
de Uteis.php assim:
{% highlight php %}
$this->config_factory->get('NOME_DA_CONFIG');
{% endhighlight %}


## Formulário de configuração do módulo

A seguir estão os passos para criamos um formulário de
configuração de um módulo, delegando para o sistema de configuração,
o armazenamento dos dados.

1 - Criando rota que aponta para ao classe do tipo Form:
{% highlight php %}
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
{% highlight php %}
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
{% highlight php %}
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


{% highlight php %}
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

### alter ID form: exemplo modificando a página de informações do site

Temos que saber o ID do formulário, aquele definido em getFormId(). 
Um caminho é identificar a rota do formulário:
{% highlight php %}
./vendor/bin/drupal debug:router| grep site-information
{% endhighlight %}

E sabendo-se a rota, podemos ver qual é a classe do formulário:
{% highlight php %}
/vendor/bin/drupal debug:router system.site_information_settings
{% endhighlight %}

Encontramos assim que o formulário está em 
*core/modules/system/src/Form/SiteInformationForm.php* 
identificamos o id retornado no método getFormId(): *system_site_information_settings*.

Em *tofu.module* podemos implementar o hook_form_ID_alter.
No nosso exemplo, vamos:
colocar um campo de texto a mais na página de configuração, validar e salvar:
{% highlight php %}
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

### Plugin: Bloco customizado

Vamos criar um plugin e esse plugin será um bloco customizado dentro
de src/Plugin/Block.

1 - Criar classe TofuBlock (src/Plugin/Block/TofuBlock.php) estendendo
BlockBase. Basta criarmos uma annotation com o id e título do bloclo.
O único método que precisamos é o build() que deve retornar um render 
array com o markup do texto que será mostrado no bloco.

{% highlight php %}
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
`$this->getConfiguration()`. Vamos aproveitar e implementar o método
blockForm para mostrar um formulário na configuração do bloco, com apenas um campo,
e blockSubmit para salvar a configuração e blockValidate para validar os campos.

{% highlight php %}
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

### Injetando services em Plugins

Tudo muito bonito. E se precisarmos injetar outro serviço que não a 
configuração? Por exemplo, o *tofu.uteis*?
Neste caso devemos implementar ContainerFactoryPluginInterface, o que nos
obriga a declarar `__construct` e `create()`, levemente diferente dos que que já vimos
até agora, pois estamos no contexto de plugins, onde temos que passar o id e plugin definition no create e no __construct.
O interessante é que ganhamos de graça a configuração,
pois ainda temos acesso `$this->setConfigurationValue('nome','valor')` e
`$this->getConfiguration()`.

Assim, particularmente, eu prefiro implementar ContainerFactoryPluginInterface 
do que BlockPluginInterface, pois fica genérico para qualquer plugin.

{% highlight php %}
namespace Drupal\tofu\Plugin\Block;

use Drupal\Core\Block\BlockBase;
use Drupal\Core\Plugin\ContainerFactoryPluginInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;
use Drupal\Core\Form\FormStateInterface;
use Drupal\tofu\Service\Uteis;
/**
 * @Block(
 *   id = "tofu_block",
 *   admin_label = @Translation("Bloco do Tofu"),
 * )
 */
class TofuBlock extends BlockBase implements ContainerFactoryPluginInterface {

  protected $uteis;
  public function __construct(array $configuration, 
    $plugin_id, $plugin_definition, Uteis $uteis){
    parent::__construct($configuration, $plugin_id, $plugin_definition);
    $this->uteis = $uteis;
  }

  public static function create(ContainerInterface $container, 
    array $configuration, $plugin_id, $plugin_definition){
    return new static (
      $configuration,
      $plugin_id, 
      $plugin_definition,
      $container->get('tofu.uteis')
    );
  }

  public function build() { 
    $config = $this->getConfiguration();
    $nome = isset($config['nome']) ? $config['nome'] : 'sem nome...';
    return [
      '#markup' => $this->t($this->uteis->inverte($nome)),
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

    if ($nome != 'Tofu1') {
      $form_state->setErrorByName('nome', t('Esse nome não é bonito!'));
    }
  }
}
{% endhighlight %}

## phpunit

Para usar o phpunit no contexto do módulo eu tive que inserir na minha instalação
do drupal de desenvolvimento as seguintes linhas no composer.json (pode ser na seção dev):

{% highlight json %}
"phpunit/phpunit": "^7",
"symfony/phpunit-bridge": "^5.1",
"behat/mink-goutte-driver": "^1.0",
"drupal/group": "^1.0"
{% endhighlight %}

Depois, copie o arquivo phpunit.xml de modelo:

{% highlight bash %}
cp web/core/phpunit.xml.dist web/core/phpunit.xml
mkdir -p /home/thiago/drupal-dev/web/sites/simpletest/browser_output
{% endhighlight %}

E configure as variáveis dentro de phpunit.xml:

- SIMPLETEST_BASE_URL: http://127.0.0.1:8088/
- SIMPLETEST_DB: sqlite://localhost//home/thiago/repos/drupal-dev/web/sites/default/files/.ht.sqlite
- BROWSERTEST_OUTPUT_DIRECTORY: /home/thiago/drupal-dev/web/sites/simpletest/browser_output

Exemplo de rodada dos testes funcionais em um módulo contrib, no caso, webform:
{% highlight bash %}
./vendor/bin/phpunit -c web/core --testsuite=functional web/modules/contrib/webform
{% endhighlight %}

Ligando flags de debug:
{% highlight bash %}
./vendor/bin/phpunit -c web/core --debug --verbose --testsuite=functional web/modules/contrib/webform
{% endhighlight %}

Também é possível apontar para um arquivo em específico:
{% highlight bash %}
./vendor/bin/phpunit -c web/core --testsuite=functional web/modules/contrib/webform/tests/src/Functional/WebformResultsExportDownloadTest.php
{% endhighlight %}

## Dicas para configurar seu ambiente

TODO: passos da instalação do phpcs
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

