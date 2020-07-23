---
title: 'Tópicos em Laravel'
date: 2020-04-10
permalink: /posts/topicos-em-laravel
categories:
  - tutorial
tags:
  - laravel
---

Pequenos trechos de códigos em laravel usados por mim com frequência, nada que substitua a documentação oficial. Incluo algumas bibliotecas que costumo usar.

<ul id="toc"></ul>

## Rotas
Route::get('/pareceristas/create','PareceristaController@create');

## Controller
php artisan make:Controller PareceristaController


## Arquivos
## Emails
## Opçãoes de lista - 
falta código para travar campo na validação in:array no form


<option value="" selected="">- Selecione -</option>
@foreach ($estagio->especifiquevtOptions() as $option)

    {{-- 1. Situação em que não houve tentativa de submissão e é uma edição --}}
    @if (old('especifiquevt') == '' and isset($estagio->especifiquevt))
    <option value="{{$option}}" {{ ( $estagio->especifiquevt == $option) ? 'selected' : ''}}>
        {{$option}}
    </option>
    {{-- 2. Situação em que houve tentativa de submissão, o valor de old prevalece --}}
    @else
    <option value="{{$option}}" {{ ( old('especifiquevt') == $option) ? 'selected' : ''}}>
        {{$option}}
    </option>
    @endif
    
@endforeach

## workflow
## seed e faker 

    $entrada = [
        'numero_usp' => 123,
        'nome' => 'Thiago Gomes Veríssimo',
    ];
    App\Parecerista::create($entrada);


return [
    'numero_usp' => $faker->unique()->numberBetween(10000, 999999),
    'nome' => $faker->name,
];

factory(App\Parecerista::class, 100)->create();

## index com busca e paginação
<form method="get" action="/pareceristas">
<div class="row">
    <div class=" col-sm input-group">
    <input type="text" class="form-control" name="busca" value="{{ Request()->busca }}">

    <span class="input-group-btn">
        <button type="submit" class="btn btn-success"> Buscar </button>
    </span>

    </div>
</div>
</form>

{{ $pareceristas->appends(request()->query())->links() }}

public function index(Request $request){
if(isset($request->busca)) {
    $pareceristas = Parecerista::where('numero_usp','LIKE',"%{$request->busca}%")->paginate(10);
} else {
    $pareceristas = Parecerista::paginate(10);
}
return view('pareceristas.index')->with('pareceristas',$pareceristas);

## Teste unitário
## mutators - get e set

public function getDivulgarAteAttribute($value) {
    /* No banco está YYYY-MM-DD, mas vamos retornar DD/MM/YYYY */
    return implode('/',array_reverse(explode('-',$value)));
}

public function setDivulgarAteAttribute($value) {
    /* Chega no formato DD/MM/YYYY e vamos salvar como YYYY-MM-DD */
    $this->attributes['divulgar_ate'] = implode('-',array_reverse(explode('/',$value)));
}

## assets
 <link rel="stylesheet" type="text/css" href="{{asset('/css/pareceristas.css')}}">

jQuery(function ($) {
    $(".cpf").mask('000.000.000-00');
});
# 
## Fila
## Foreign Key - model - relacionamento
## Validações
php artisan make:request PareceristaRequest
$validated = $request->validated();

# CRUD completo 
php artisan make:model Parecerista -a
public function edit(Parecerista $parecerista){
    return view('pareceristas.edit')->with('parecerista',$parecerista);
}

## Login - como
## Mensagens de flash
old('numero_usp',$parecerista->numero_usp)

## Rota assinada
## GATE - permissões



## Bibliotecas gerais
### Gerador de fakers
### Biblioteca para PDF
### Biblioteca para Excel


 Exemplos com rotas

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

## Biblioteca para PDF

{% highlight bash %}
composer require barryvdh/laravel-dompdf
php artisan vendor:publish --provider="Barryvdh\DomPDF\ServiceProvider"
mkdir resources/views/pdfs/
touch resources/views/pdfs/exemplo.blade.php
{% endhighlight %}

No controller:

{% highlight bash %}
use PDF;
public function convenio(Convenio $convenio){
    $exemplo = 'Um pdf banaca';
    $pdf = PDF::loadView('pdfs.exemplo', compact('exemplo'));
    return $pdf->download('exemplo.pdf');
}
{% endhighlight %}

Por fim, agora pode escrever sua estrutura do pdf, mas usando blade
exemplo.blade.php:

{% highlight php %}
{% raw %}
{{ $exemplo }}
{% endraw %}
{% endhighlight %}


## Biblioteca para Excel

Instalação
{% highlight bash %}
composer require maatwebsite/excel
mkdir app/Exports
touch app/Exports/ExcelExport.php
{% endhighlight %}

Implementar uma classe que recebe um array multidimensional com os dados, linha a linha.
E outro array com os títulos;
{% highlight php %}
namespace App\Exports;

use Maatwebsite\Excel\Concerns\FromArray;
use Maatwebsite\Excel\Concerns\WithHeadings;

class ExcelExport implements FromArray, WithHeadings
{
    protected $data;
    protected $headings;
    public function __construct($data, $headings){
        $this->data = $data;
        $this->headings = $headings;
    }

    public function array(): array
    {
        return $this->data;
    }

    public function headings() : array
    {
        return $this->headings;
    }
}
{% endhighlight %}

Usando no controller:
{% highlight php %}
use Maatwebsite\Excel\Excel;
use App\Exports\ExcelExport;

public function exemplo(Excel $excel){
  
  $headings = ['ano','aprovados','reprovados'];
  $data = [
      [2000,12,15],
      [2001,10,11],
      [2002,11,21]
    ];
    $export = new ExcelExport($data,$headings);
    return $excel->download($export, 'exemplo.xlsx');
}

public function export($format){
}
{% endhighlight %}


## Relação das bibliotecas aqui usadas

    composer require appzcoder/crud-generator --dev
    composer require mpociot/laravel-test-factory-helper --dev
    composer require laracasts/generators --dev
    
    composer require laravellegends/pt-br-validator

 ## Bibliotecas USP

 Essa relação é exclusiva para quem trabalha na Universidade de São Paulo.

    composer require uspdev/senhaunica-socialite
    composer require uspdev/laravel-usp-validators
    composer require uspdev/replicado
    composer require uspdev/laravel-usp-theme
    composer require uspdev/laravel-usp-faker --dev
    
## Gerador de fakers

https://github.com/mpociot/laravel-test-factory-helper

Insedir como o seed chama o faker.

gerador de tabebas pivot:
https://github.com/laracasts/Laravel-5-Generators-Extended/


