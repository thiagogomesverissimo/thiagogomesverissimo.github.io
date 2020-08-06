---
title: 'Tópicos em Laravel'
date: 2020-04-10
permalink: /posts/topicos-em-laravel
categories:
  - tutorial
tags:
  - laravel
---

Pequenos trechos de códigos em laravel usados por mim com frequência, nada que substitua a documentação oficial.

<ul id="toc"></ul>

## Rotas

Exemplo geral de uma rota do tipo GET:
{% highlight php %}
Route::get('/livros/create','LivroController@create');
{% endhighlight %}

Exemplo com REGEX que só aceita número inteiro no parâmetro id:
{% highlight php %}
Route::get('users/{id}',function($id){
    return $id;
})->where('id','[0-9]+');
{% endhighlight %}

Exemplo com REGEX que só aceita letras no parâmetro username:
{% highlight php %}
Route::get('users/{username}',function($username){
    return $username;
})->where('username','[A-Za-z]+');
{% endhighlight %}

Exemplo que aceita uma parâmetro somente com inteiro e outro somente com letra:
{% highlight php %}
Route::get('posts/{id}/{slug}',function($id,$slug){
    return $slug . ' ' .  $id;
})->where([
    'id' => '[0-9]+',
    'slug' => '[A-Za-z]+'
]);
{% endhighlight %}

## Migrations

Adicionando coluna `editora` em uma tabela existente chamada `livros`:
{% highlight bash %}
php artisan make:migration add_editora_to_livros_table  --table=livros
{% endhighlight %}

## Autenticação

O laravel tem um mecanismo de criar todo o esquema de autenticação
automaticamente. Como eu sempre precisei customizá-lo, 
acabo criando eu mesmo o controller, views, migrations etc.

Primeiramente, o método de login `auth()->login($user)` 
ou `Auth::login($user)`, que pode ser usado no controler espera 
um objeto da classe `Illuminate\Foundation\Auth\User`.
Por padrão, o model `User` criado automaticamente na instalação
já estende essa classe. A migration corresnpondente também já estão ok padrão.
Vou mostrar apenas o procedimento de login, pois, estou supondo
que a tabela de `users` é populada por alguma outra fonte qualquer.

Supondo que a única coisa que você precisa fazer no seu controller é logar
o usuário e que você já fez a conferência que o usuário é o próprio 
(talvez seja um retorno de OAuth), você faria algo do tipo:
{% highlight php %}
$user = User::where('email',$email)->first()
if (is_null($user)) $user = new User;
$user->name  = $name;
$user->email = $email;
$user->save();
auth()->login($user);
return redirect('/');
{% endhighlight %}

Para login local, apesar de são ser obrigatório, pode ser útil usar 
a trait `Illuminate\Foundation\Auth\AuthenticatesUsers` que está no
pacote:

{% highlight bash %}
composer require laravel/ui
{% endhighlight %}

Usando a trait `AuthenticatesUsers` no seu controller você ganha os métodos:

- showLoginForm(): requisição GET apontando para auth/login.blade.php 
- login(): requisição POST que recebe `email` e `password` e chama `auth()->login($user)`

Assim, basta criarmos as rotas correspondentes:
{% highlight php %}
Route::get('login', 'LoginController@showLoginForm')->name('login');
Route::post('login', 'LoginController@login');
{% endhighlight %}

Seu LoginController ficaria assim nesse caso:
{% highlight php %}
use Illuminate\Foundation\Auth\AuthenticatesUsers;
class LoginController extends Controller
{
    use AuthenticatesUsers;
    protected $redirectTo = '/';
}
{% endhighlight %}

Ainda no LoginController, se o campo que você for receber em `login()`, 
não for o `email`, mas sim `codigo_usuario`, pode fazer a mudança em:
{% highlight php %}
public function username()
{
    return 'codigo_usuario';
}
{% endhighlight %}

A forma mais rápida de criar um usuário para teste é pelo `php artisan tinker`:
{% highlight php %}
$user = new App\User;
$user->email = 'teste2@teste.com'
$user->name = 'Maria'
$user->password = bcrypt('123')
$user->codigo_usuario = '999222'
$user->save()
{% endhighlight %}

For fim, um formulário para login:

{% highlight html %}
{% raw %}
<form method="POST" action="/login">
    @csrf
    
    <div class="form-group row">
        <label for="codigo_usuario" class="col-sm-4 col-form-label text-md-right">codigo_usuario</label>

        <div class="col-md-6">
            <input type="text" name="codigo_usuario" value="{{ old('codigo_usuario') }}" required>
        </div>
    </div>

    <div class="form-group row">
        <label for="password" class="col-md-4 col-form-label text-md-right">Senha</label>

        <div class="col-md-6">
            <input type="password" name="password" required>
        </div>
    </div>

    <div class="form-group row mb-0">
        <div class="col-md-8 offset-md-4">
            <button type="submit" class="btn btn-primary">Entrar</button>
        </div>
    </div>
</form>
{% endraw %}
{% endhighlight %}

### Implementação do logout

Uma boa prática é implementar o logout usando uma requisição POST.
Segue um rascunho do formulário com o botão para logout:
{% highlight html %}
{% raw %}
<form action="/logout" method="POST" class="form-inline" 
    style="display:inline-block" id="logout_form">
    @csrf
    <!-- O uso do link ao invés do botao é para poder formatar corretamente -->
    <a onclick="document.getElementById('logout_form').submit(); return false;"
        class="font-weight-bold text-white nounderline pr-2 pl-2" href>Sair</a>
</form>
{% endraw %}
{% endhighlight %}

O método no controller é bem simples:
{% highlight php %}
public function logout()
{
    auth()->logout();
    return redirect('/');
}
{% endhighlight %}

## Autorização




## Arquivos
## Emails

## Opções de lista
falta código para travar campo na validação in:array no form

{% highlight html %}
{% raw %}
<option value="" selected=""> - Selecione  -</option>
@foreach ($livro->categorias() as $categoria)

    {{-- 1. Situação em que não houve tentativa de submissão e é uma edição --}}
    @if (old('categoria') == '' and isset($livro->categoria))
    <option value="{{$categoria}}" {{ ( $livro->categoria == $categoria) ? 'selected' : ''}}>
        {{$categoria}}
    </option>
    {{-- 2. Situação em que houve tentativa de submissão, o valor de old prevalece --}}
    @else
    <option value="{{$categoria}}" {{ ( old('categoria') == $option) ? 'selected' : ''}}>
        {{$option}}
    </option>
    @endif
    
@endforeach
{% endraw %}
{% endhighlight %}


## workflow
## seed e faker 

{% highlight php %}
{% raw %}
    $entrada = [
        'numero_usp' => 123,
        'nome' => 'Thiago Gomes Veríssimo',
    ];
    App\Parecerista::create($entrada);


return [
    'numero_usp' => $faker->unique()->numberBetween(10000, 999999),
    'nome' => $faker->name,
];
{% endraw %}
{% endhighlight %}

factory(App\Parecerista::class, 100)->create();

## index com busca e paginação
{% highlight html %}
{% raw %}
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
{% endraw %}
{% endhighlight %}


{% highlight php %}
public function index(Request $request){
if(isset($request->busca)) {
    $pareceristas = Parecerista::where('numero_usp','LIKE',"%{$request->busca}%")->paginate(10);
} else {
    $pareceristas = Parecerista::paginate(10);
}
return view('pareceristas.index')->with('pareceristas',$pareceristas);

{% endhighlight %}

## Teste unitário
## mutators - get e set

{% highlight php %}


public function getDivulgarAteAttribute($value) {
    /* No banco está YYYY-MM-DD, mas vamos retornar DD/MM/YYYY */
    return implode('/',array_reverse(explode('-',$value)));
}

public function setDivulgarAteAttribute($value) {
    /* Chega no formato DD/MM/YYYY e vamos salvar como YYYY-MM-DD */
    $this->attributes['divulgar_ate'] = implode('-',array_reverse(explode('/',$value)));
}

{% endhighlight %}

## assets
{% highlight css %}
{% raw %}
 <link rel="stylesheet" type="text/css" href="{{asset('/css/pareceristas.css')}}">

jQuery(function ($) {
    $(".cpf").mask('000.000.000-00');
});
{% endraw %}
{% endhighlight %}
# 
## Fila
## Foreign Key - model - relacionamento
## Validações
php artisan make:request PareceristaRequest
$validated = $request->validated();

# CRUD completo 
{% highlight php %}
php artisan make:model Parecerista -a
public function edit(Parecerista $parecerista){
    return view('pareceristas.edit')->with('parecerista',$parecerista);
}
{% endhighlight %}


## Mensagens de flash
old('numero_usp',$parecerista->numero_usp)

{% highlight html %}
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


## Rota assinada
## GATE - permissões



## Bibliotecas gerais
### Gerador de fakers
### Biblioteca para PDF
### Biblioteca para Excel




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
{% raw %}
<form method="POST" enctype="multipart/form-data">
  <input type="file" name="certificado">
</form>
{% endraw %}
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
{% raw %}
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
{% endraw %}
{% endhighlight %}

Usando no controller:
{% highlight php %}
{% raw %}
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
{% endraw %}
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


