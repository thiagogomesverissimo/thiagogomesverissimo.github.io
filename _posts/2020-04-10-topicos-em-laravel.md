---
title: 'Tópicos em Laravel'
date: 2020-04-10
permalink: /posts/topicos-em-laravel
categories:
  - tutorial
tags:
  - laravel
---

Pequenos trechos de códigos em laravel usados por mim com frequência, nada que substitua a documentação oficial. Incluo algumas bibliotecas que aceleram o processo de desenvolvimento.

<ul id="toc"></ul>

## Geradores de códigos

Suponham que precisamos gerar todo fluxo para um sistema de cadastro de livros, o famoso CRUD. Geradores de códigos são polêmicos, muitas vezes genéricos demais, mas eu prefiro usá-los. O importante é ter em mente que eles não farão seu sistema, mas sim te darão um ponto de partida. 

Usando a biblioteca *crud-generator* você pode criar um arquivo json com a definição dos seus campos, desta maneira:
{% highlight yml %}
{
    "fields": [
        {
            "name": "titulo",
            "type": "string"
        },
        {
            "name": "resumo",
            "type": "text"
        },
        {
            "name": "publicado_em",
            "type": "date"
        },
        {
            "name": "acesso_aberto",
            "type": "radio"
        },
        {
            "name": "capa",
            "type": "file"
        },
        {
            "name": "area",
            "type": "select",
            "options": {
                "filosofia_medieval": "Filosofia Medieval",
                "historia_ocidental": "História Ocidental",
                "geografia_fisica": "Geografia Física"
            }
        }
    ]
}
{% endhighlight %}

O que eu normalmente mudo no código gerado:

 - O template pai (ou mãe), assim troco a lista extends
 - A opção de seleção em lista, mando para ao model
 - uso typehint no controller para carregar os models
 - Eu não uso a opção de validação dentro do controller, pois faço com FormRequest

https://github.com/InfyOmLabs/laravel-generator

???

## Gerador de fakers

https://github.com/mpociot/laravel-test-factory-helper

Insedir como o seed chama o faker.

gerador de tabebas pivot:
https://github.com/laracasts/Laravel-5-Generators-Extended/



## Exemplos com rotas

Exemplo de REGEX que só aceita número inteiro no parâmetro id:
{% highlight php %}
Route::get('users/{id}',function($id){
    return $id;
})->where('id','[0-9]+');
{% endhighlight %}

Exemplo de REGEX que só aceita letras no parâmetro username:
{% highlight php %}
Route::get('users/{username}',function($username){
    return $username;
})->where('username','[A-Za-z]+');
{% endhighlight %}

Rota que aceita uma parâmetro somente com inteiro e outro somente com
letra:
{% highlight php %}
Route::get('posts/{id}/{slug}',function($id,$slug){
    return $slug . ' ' .  $id;
})->where([
    'id' => '[0-9]+',
    'slug' => '[A-Za-z]+'
]);
{% endhighlight %}

## Três formas de fazer validações

Quando estamos dentro de um método do controller podemos usar *$this->validate*,
que validará os campos com a condições que passaremos e caso falhe a validação: 1 - Automaticamente retornará o usuário para página de origem. 2 - Devolverá para página de origem os inputs enviados na requisição. 3 - Enviará para página de origem as mensagens de erro da validação. Para tudo isso ocorrer, basta fazermos:
{% highlight php %}
$request->validade([
  'nome' => 'required'
]);
{% endhighlight %}

Uma segunda maneira de validar é usar diretamente a classe Validator, neste caso temos que fazer o redirect para a origem da requisição por nossa conta com os inputs e erros relacioandos:
{% highlight php %}
use Illuminate\Support\Facades\Validator;
...
$validator = Validator::make($request->all(),[
  'nome' => 'required'
]);
if($validator->fails()){
  return redirect('/node/create')
          ->withErrors($validator)
          ->withInput();
}
{% endhighlight %}

O terceiro método, mais elegante, é criar uma classe do tipo FormRequest, em
app/Http/Requests e delegar a validação dos campos para o método rules() dessa classe. Pode-se criar um FormRequest com o artisan:
{% highlight bash %}
php artisan make:request EmpresaRequest
{% endhighlight %}

Coloque no retorno de rules() suas validações:
{% highlight php %}
namespace App\Http\Requests;
use Illuminate\Foundation\Http\FormRequest;
class EmpresaRequest extends FormRequest
{
    public function rules(){
        return [
          'nome' => 'required',
          'cnpj' => 'required',
        ];
    };
}
{% endhighlight %}

Por fim, no método do controller que receberá os dados, 
injete o FormRequest. No formRequest existe um método chamado
validated() que devolve um array com os dados validados, que pode
ser então usado para salvar no banco com seu model, com o método create.
{% highlight php %}
public function store(EmpresaRequest $request){
    $validated = $request->validated();
    Empresa::create($validated);
}
{% endhighlight %}

## Mensagens de flash
O laravel mantém em qualquer request uma variável *$error*
que pode ser usada para mostrar um alert com classes do bootstrap. 
Usando Session::has também pegamos outros tipos de mensagens:
{% highlight php %}
{% raw %}
@if ($errors->any())
  <div class="alert alert-danger">
    <ul>
      @foreach ($errors->all() as $error)
        <li>{{ $error }}</li>
      @endforeach
    </ul>
  </div>
@endif

<div class="flash-message">
  @foreach (['danger', 'warning', 'success', 'info'] as $msg)
    @if(Session::has('alert-' . $msg))
      <p class="alert alert-{{ $msg }}">{{ Session::get('alert-' . $msg) }}
        <a href="#" class="close" data-dismiss="alert" aria-label="fechar">&times;</a>
      </p>
    @endif
  @endforeach
</div>
{% endraw %}
{% endhighlight %}

# Arquivos

Campo para upload do arquivo no formulário html:
{% highlight html %}
<form method="POST" enctype="multipart/form-data">
  <input type="file" name="certificado">
</form>
{% endhighlight %}

A validação de arquivos deve ser feita assim:
{% highlight php %}
if($request->hasFile('certificado')){

}
{% endhighlight %}

Devolvendo um response com um arquivo para o browser:
{% highlight php %}
Route::get('pdf',function(){
    return response()->file('/tmp/teste.pdf');
});
{% endhighlight %}

## Relação das bibliotecas aqui usadas

    composer require appzcoder/crud-generator --dev
    composer require mpociot/laravel-test-factory-helper --dev
    composer require laracasts/generators --dev
    composer require barryvdh/laravel-dompdf
    composer require laravellegends/pt-br-validator

 ## Bibliotecas USP

 Essa relação é exclusiva para quem trabalha na Universidade de São Paulo.

    composer require uspdev/senhaunica-socialite
    composer require uspdev/laravel-usp-validators
    composer require uspdev/replicado
    composer require uspdev/laravel-usp-theme
    composer require uspdev/laravel-usp-faker --dev
    
