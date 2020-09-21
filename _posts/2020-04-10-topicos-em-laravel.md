---
title: 'Tópicos em Laravel'
date: 2020-04-10
permalink: /posts/topicos-em-laravel
categories:
  - tutorial
tags:
  - laravel
---

Pequenos trechos de códigos em laravel usados por mim com frequência, nada 
que substitua a documentação oficial. Está estruturado para utilização em 
oficinas de introdução ao framework numa perspectiva mais genérica.
Assim, é possível encontrar certas omissões propositais ou práticas não comuns
na comunidade, que são tratadas no contexto das oficinas.

<br>
<ul id="toc"></ul>


## 1: MVC - Model View Controller

### 1.1: Request e Response ou Pergunta e Resposta

Criando uma rota para recebimento das requisições.
{% highlight php %}
Route::get('/livros', function () {
    echo "Não há livros cadastrados nesses sistema ainda!";
});
{% endhighlight %}

### 1.2: Controller

Vamos começar a espalhar mais o tratamento das requisições em uma arquitetura
convencional?

Criando um controller:
{% highlight bash %}
php artisan make:controller LivroController
{% endhighlight %}
O arquivo criado está em `app/Http/Controllers/LivroController.php`.

Vamos criar um método chamado `index()` dentro do controller gerado:
{% highlight php %}
public function index(){
    return "Não há livros cadastrados nesses sistema ainda!";
}
{% endhighlight %}

Vamos alterar nossa rota para apontar para o método `index()`
do `LivroController`:

{% highlight php %}
use App\Http\Controllers\LivroController;
Route::get('/livros', [LivroController::class,'index']);
{% endhighlight %}

E se quisermos passar uma parâmetro no endereço da requisição?
Exemplo, suponha que o ISBN do livro "Quincas Borba" seja 9780195106817.
Se fizermos `/livros/9780195106817` queremos que nosso sistema identifique
o livro.

Assim, vamos adicionar um novo método chamado `show($isbn)` que recebe o isbn
e deverá fazer a lógica de identificação do livro.

{% highlight php %}
public function show($isbn){
    if($isbn == '9780195106817') {
        return "Quincas Borba - Machado de Assis";
    } else {
        return "Livro não identificado";
    }
}
{% endhighlight %}

Por fim, adicionemos a rota prevendo o recebimento do isbn:
{% highlight php %}
Route::get('/livros/{isbn}', [LivroController::class, 'show']);
{% endhighlight %}

### 1.3. View: Blade

Vamos melhorar os retornos do controller?
A principal característica do sistema de template é a herança. Então, vamos
começar criando um template principal `resources/view/main.blade.php` 
com seções genéricas:

{% highlight html %}
{% raw %}
<!DOCTYPE html>
<html>
    <head>
        <title>@section('title') Exemplo @show</title>
    </head>
    <body>
        @yield('content')
    </body>
</html>
{% endraw %}
{% endhighlight %}

Primeiramente, vamos criar o template para o index `resources/views/livros/index.blade.php`:
obedecendo a estrutura:

{% highlight html %}
{% raw %}
@extends('main')
@section('content')
  Não há livros cadastrados nesse sistema ainda!
@endsection
{% endraw %}
{% endhighlight %}

E mudamos o controller para chamar essa view:
{% highlight php %}
public function index(){
    return view(livros.index);
}
{% endhighlight %}

Podemos enviar variáveis diretamente para o template e com alguma
cautela, podemos até implementar parte da lógica do nosso sistema no template,
pois o blade é uma linguagem de programação:

{% highlight php %}
public function show($isbn){
    if($isbn == '9780195106817') {
        $livro = "Quincas Borba - Machado de Assis";
    } else {
        $livro = "Livro não identificado";
    }
    return view('livros.show', [
        'livro' => $livro
    ]);
}
{% endhighlight %}

O template `resources/views/livros/show.blade.php` ficará assim:

{% highlight html %}
{% raw %}
@extends('main')
@section('content')
  {{ $livro }}
@endsection
{% endraw %}
{% endhighlight %}

### 1.4: Model

Vamos inserir nossos livros no banco de dados?
Para tal, vamos criar uma tabela chamada `livros` no banco dados 
por intermédio de uma migration e um model `Livro` para operarmos nessa tabela.

{% highlight bash %}
php artisan make:migration create_livros_table --create='livros'
php artisan make:model Livro
{% endhighlight %}

Na migration criada vamos inserir os campos: titulo, autor e isbn,
deixando o autor como opcional.

{% highlight php %}
$table->string('titulo');
$table->string('autor')->nullable();
$table->string('isbn');
{% endhighlight %}

Usando uma espécie de `shell` do laravel, o tinker, vamos inserir
o registro do livro do Quincas Borba:

{% highlight bash %}
php artisan tinker
$livro = new App\Models\Livro;
$livro->titulo = "Quincas Borba";
$livro->autor = "Machado de Assis";
$livro->isbn = "9780195106817";
$livro->save();
quit
{% endhighlight %}

Insira mais livros!
Veja que o model `Livro` salvou os dados na tabela `livros`. Estranho não?
Essa é uma da inúmeras convenções que vamos nos deparar ao usar um framework.

Vamos modificar o controller para operar com os livros do banco de dados?
No método index vamos buscar todos livros no banco de dados e enviar para
o template:
{% highlight php %}
public function index(){
    $livros = App\Models\Livro:all();
    return view('livros.index',[
        'livros' => $livros
    ]);
}
{% endhighlight %}

No template podemos iterar sobre todos livros recebidos do controller:
{% highlight php %}
{% raw %}
@forelse ($livros as $livro)
    <li>{{ $livro->titulo }}</li>
    <li>{{ $livro->autor }}</li>
    <li>{{ $livro->isbn }}</li>
@empty
    Não há livros cadastrados
@endforelse
{% endraw %}
{% endhighlight %}

No método `show` vamos buscar o livro com o isbn recebido e entregá-lo
para o template:

{% highlight php %}
public function show($isbn){
    $livro = App\Moldes\Livro::where('isbn',$isbn)->first();
        return view('livros.show',[
            'livro' => $livro
        ]);
}
{% endhighlight %}

No template vamos somente mostrar o livro:
{% highlight php %}
{% raw %}
<li>{{ $livro->titulo }}</li>
<li>{{ $livro->autor }}</li>
<li>{{ $livro->isbn }}</li>
{% endraw %}
{% endhighlight %}

Perceba que parte do código está repetida no index e no show do blade.
Para melhor organização é comum criar um diretório `resources/views/livros/partials`
para colocar pedaços de templates. Neste caso poderia ser 
`resources/views/livros/partials/fields.blade.php` e nos templates index e show
o chamaríamos como:

{% highlight php %}
{% raw %}
@include('livros.partials.fields')
{% endraw %}
{% endhighlight %}

### 1.5: Fakers

Durante o processo de desenvolvimento precisamos manipular dados
constantemente, então é uma boa ideia gerar alguns dados aleatórios (faker)
e outros controlados (seed) para não termos que sempre criá-los manualmente: dqw

{% highlight bash %}
php artisan make:factory LivroFactory --model='Livro'
php artisan make:seed LivroSeeder
{% endhighlight %}

Inicialmente, vamos definir um padrão para geração de
dados aleatório `database/factories/LivroFactory.php`:

{% highlight php %}
return [
    'titulo' => $this->faker->sentence(3),
    'isbn'   => $this->faker->ean13(),
    'autor'  => $this->faker->name
];
{% endhighlight %}

Em `database/seeders/LivroSeeder.php` vamos criar ao menos um registro
de controle e chamar o factory para criação de 150 registros aleatórios.

{% highlight php %}
$livro = [
    'titulo' => "Quincas Borba",
    'autor'  => "Machado de Assis",
    'isbn'       => "9780195106817"
];
\App\Models\Livro::create($livro);
\App\Models\Livro::factory(150)->create();
{% endhighlight %}

Rode o seed e veja que os dados foram criados:
{% highlight bash %}
php artisan db:seed --class=LivroSeeder
{% endhighlight %}

Depois de testado e funcionando insirá seu seed em 
`database/seeders/DatabaseSeeder` para ser chamado globalmente:

{% highlight php %}
public function run()
{
    $this->call([
        UserSeeder::class,
        LivroSeeder::class
    ]);
}
{% endhighlight %}

Se precisar zerar o banco e subir todos os seeds na sequência:
{% highlight bash %}
php artisan migrate:fresh --seed
{% endhighlight %}

### 1.6: Exercício MVC

- Implementação de um model chamado `LivroFulano`, onde `Fulano` é um identificador
seu. 
- Implementar a migration correspondente com os campos: titulo, autor e isbn.
- Implementar seed com ao menos um livro de controle
- Implementar o faker com ao menos 100 livros
- Implementar controller com os métodos index e show com respectivos templates e rotas
- Implementar os templates (blades) correspondentes

## 2: CRUD: Create (Criação), Read (Consulta), Update (Atualização) e Delete (Destruição)

### 2.1: Limpando ambiente

Neste ponto conhecemos um pouco do jargão e da estrutura usada pelo laravel para 
implementar a arquitetura MVC.
Frameworks como o laravel são flexíveis o suficiente para serem customizados ao seu gosto.
Porém, sou partidário da ideia de seguir convenções quando possível. Por isso começaremos
criando a estrutura básica para implementar um CRUD clássico na forma mais simples.
Esse CRUD será modificado ao longo do texto.

Apague (faça backup se quiser) o model, controller, seed, factory e migration,
mas não delete os arquivos blades, pois eles serão reutilizados:

{% highlight bash %}
rm app/Models/Livro.php
rm app/Http/Controllers/LivroController.php
rm database/seeders/LivroSeeder.php
rm database/factories/LivroFactory.php
rm database/migrations/202000000000_create_livros_table.php
{% endhighlight %}

### 2.1: Criando model, migration, controller, faker e seed para implementação do CRUD

Vamos recriar tudo novamente usando o comando:
{% highlight bash %}
php artisan make:model Livro --all
{% endhighlight %}

Perceba que a migration, o faker, o seed e o controller estão automaticamente
conectados ao model Livro. E mais, o controller contém todos métodos
necessários para as operações do CRUD, chamado do laravel de `resource`.
Ao invés de especificarmos uma a uma a rota para cada operação, podemos
simplesmente seguir a convenção e substituir a definição anterior por:

{% highlight php %}
Route::resource('livros', LivroController::class);
{% endhighlight %}

Segue uma implementação simples de cada operação:
{% highlight php %}
public function index()
{
    $livros =  Livro::all();
    return view('livros.index',[
        'livros' => $livros
    ]);
}

public function create()
{
    return view('livros.create',[
        'livro' => new Livro,
    ]);
}

public function store(Request $request)
{
    $livro = new Livro;
    $livro->titulo = $request->titulo;
    $livro->autor = $request->autor;
    $livro->isbn = $request->isbn;
    $livro->save();
    return redirect("/livros/{$livro->id}");
}

public function show(Livro $livro)
{
    return view('livros.show',[
        'livro' => $livro
    ]);
}

public function edit(Livro $livro)
{
    return view('livros.edit',[
        'livro' => $livro
    ]);
}

public function update(Request $request, Livro $livro)
{
    $livro->titulo = $request->titulo;
    $livro->autor = $request->autor;
    $livro->isbn = $request->isbn;
    $livro->save();
    return redirect("/livros/{$livro->id}");
}

public function destroy(Livro $livro)
{
    $livro->delete();
    return redirect('/livros');
}
{% endhighlight %}

Criando os arquivos blades:

{% highlight bash %}
mkdir -p resources/views/livros/partials
cd resources/views/livros
touch index.blade.php create.blade.php edit.blade.php show.blade.php 
touch partials/form.blade.php partials/fields.blade.php
{% endhighlight %}

Um implementação básica de cada template:
{% highlight html %}
{% raw %}

<!-- ###### partials/fields.blade.php ###### -->
<ul>
  <li><a href="/livros/{{$livro->id}}">{{ $livro->titulo }}</a></li>
  <li>{{ $livro->autor }}</li>
  <li>{{ $livro->isbn }}</li>
  <li>
    <form action="/livros/{{ $livro->id }} " method="post">
      @csrf
      @method('delete')
      <button type="submit" onclick="return confirm('Tem certeza?');">Apagar</button> 
    </form>
  </li> 
</ul>

<!-- ###### index.blade.php ###### -->
@extends('main')
@section('content')
  @forelse ($livros as $livro)
    @include('livros.partials.fields')
  @empty
    Não há livros cadastrados
  @endforelse
@endsection

<!-- ###### show.blade.php ###### -->
@extends('main')
@section('content')
  @include('livros.partials.fields')
@endsection  

<!-- ###### partials/form.blade.php ###### -->
Título: <input type="text" name="titulo" value="{{ $livro->titulo }}">
Autor: <input type="text" name="autor" value="{{ $livro->autor }}">
ISBN: <input type="text" name="isbn" value="{{ $livro->isbn }}">
<button type="submit">Enviar</button>

<!-- ###### create.blade.php ###### -->
@extends('main')
@section('content')
  <form method="POST" action="/livros">
    @csrf
    @include('livros.partials.form')
  </form>
@endsection

<!-- ###### edit.blade.php ###### -->
@extends('main')
@section('content')
  <form method="POST" action="/livros/{{ $livro->id }}">
    @csrf
    @method('patch')
    @include('livros.partials.form')
  </form>
@endsection

{% endraw %}
{% endhighlight %}

Conhecendo o sistema de herança do blade, podemos extender qualquer template,
inclusive de biblioteca externas. Existem diversas implementações do AdminLTE na
internet e você pode implementar uma para sua empresa, por exemplo. Aqui vamos
usar [https://github.com/uspdev/laravel-usp-theme](https://github.com/uspdev/laravel-usp-theme). 
Consulte a documentação para informações de como instalá-la. No nosso 
template principal `main.blade.php` vamos apagar o que tínhamos antes e
apenas extender essa biblioteca:

{% highlight html %}
{% raw %}
@extends('laravel-usp-theme::master')
{% endraw %}
{% endhighlight %}

Dentre outras vantagens, ganhamos automaticamente o carregamento de frameworks
como o bootstrap e fontawesome.

### 2.3: Exercício CRUD

- Implementação de um CRUD completo para o model `LivroFulano`, onde `Fulano` é um identificador
seu. 
- Todas operações devem funcionar: criar, editar, ver, listar e apagar

## 3: Validação

### 3.1: Mensagens flash

Da maneira como implementamos o CRUD até então, qualquer valor que o usuário
digitar no cadastro ou edição será diretamente enviado ao banco da dados.
Vamos colocar algumas regras de validação no meio do caminho.
Por padrão, em todo arquivo blade existe o array `$errors` que é sempre
inicializado pelo laravel. Quando uma requisição não passar na validação, o laravel
colocará as mensagens de erro nesse array automaticamente. Assim, basta que no
nosso arquivo principal do blade, façamos uma iteração nesse array:

{% highlight html %}
{% raw %}
@section('flash')
    @if ($errors->any())
    <div class="alert alert-danger">
        <ul>
            @foreach ($errors->all() as $error)
            <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
    @endif
@endsection
{% endraw %}
{% endhighlight %}

Além disso, podemos manualmente no nosso controller enviar uma mensagem `flash`
para o sessão assim: `request()->session()->flash('alert-info','Livro cadastrado com sucesso')`.
Como nosso template principal usa o boostrap, podemos estilizar nossas
mensagens flash com os valores danger, warning, success e info:

{% highlight html %}
{% raw %}
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

### 3.2: Validação no Controller

Quando estamos dentro de um método do controller, a forma mais rápida de validação é
usando `$request->validate`, que validará os campos com as condições que 
passaremos e caso falhe a validação, automaticamente o usuário é retornado 
para página de origem com todos inputs que foram enviados na requisição, além da
mensagens de erro:

{% highlight php %}
$request->validade([
  'titulo' => 'required',
  'autor' => 'required',
  'isbn' => 'required|integer',
]);
{% endhighlight %}

Podemos usar a função `old('titulo',$livro->titulo)` nos formulários, que 
verifica que a inputs na sessão e em caso negativo usa o segundo parâmetro.
Assim, podemos deixar o partials/form.blade.php mais elegante:

{% highlight html %}
{% raw %}
Título: <input type="text" name="titulo" value="{{old('titulo', $livro->titulo)}}">
Autor: <input type="text" name="autor" value="{{old('autor', $livro->autor)}}">
ISBN: <input type="text" name="isbn" value="{{old('isbn', $livro->isbn)}}">
{% endraw %}
{% endhighlight %}

### 3.3: Validação com a classe Validator

O `$request->validate` faz tudo para nós. Mas se por algum motivo você precisar
interceder na validação, no que é retornado e para a onde, pode-se usar
diretamente `Illuminate\Support\Facades\Validator`:

{% highlight php %}
use Illuminate\Support\Facades\Validator;
...
$validator = Validator::make($request->all(),[
  'titulo' => 'required'
]);
if($validator->fails()){
  return redirect('/node/create')
          ->withErrors($validator)
          ->withInput();
}
{% endhighlight %}

### 3.4: FormRequest

Se olharmos bem para os métodos store e update veremos que eles
são muito próximos. Se tivéssemos uns 20 campos, esses dois métodos
cresceriam juntos, proporcionalmente. Ao invés de atribuirmos campo
a campo a criação ou edição de um livro, vamos fazer uma atribuição 
em massa, para isso, no model vamos proteger o id, isto é, numa atribuição
em massa, o id não poderá ser alterado, em `app/Models/Livro.php`
adicione a linha `protected $guarded = ['id'];`.

A validação, que muitas vezes será idêntica no store e no update, vamos
delegar para um FormRequest. Crie um FormRequest com o artisan:
{% highlight bash %}
php artisan make:request LivroRequest
{% endhighlight %}

Esse comando gerou o arquivo `app/Http/Requests/LivroRequest.php`. Como
ainda não falamos de autenticação e autorização, retorne `true` no método
`authorize()`. As validações podem ser implementada em `rules()`.
Perceba que o isbn pode ser digitado com traços ou ponto, mas eu
só quero validar a parte numérica do campo e ignorar o resto, 
para isso usei o método `prepareForValidation`:

{% highlight php %}
public function rules(){
    $rules = [
        'titulo' => 'required',
        'autor'  => 'required',
        'isbn' => 'required|integer',
    ];
}
protected function prepareForValidation()
{
    $this->merge([
        'isnb' => preg_replace('/[^0-9]/', '', $this->isnb),
    ]);
}
{% endhighlight %}

Não queremos livros cadastrados com o mesmo isbn. Há uma validação
chamada `unique` que pode ser invocada na criação de um livro como 
`unique:TABELA:CAMPO`, mas na edição, temos que ignorar o próprio livro
assim `unique:TABELA:CAMPO:ID_IGNORADO`. Dependendo do
seu projeto, talvez seja melhor fazer um formRequest para criação e 
outro para edição. Eu normalmente uso apenas um para ambos. Como abaixo,
veja que as mensagens de erros podem ser customizadas com o método
`messages()`:

{% highlight php %}
public function rules(){
    $rules = [
        'titulo' => 'required',
        'autor'  => 'required',
        'isnb' => ['required','integer'],
    ];
    if ($this->method() == 'PATCH' || $this->method() == 'PUT'){
        array_push($rules['isnb'], 'unique:livros,isnb,' .$this->id);
    }
    else{
        array_push($rules['isnb'], 'unique:livros');
    }
}
protected function prepareForValidation()
{
    $this->merge([
        'isnb' => preg_replace('/[^0-9]/', '', $this->isnb),
    ]);
}
public function messages()
{
    return [
        'cnpj.unique' => 'Este isnb está cadastrado para outro livro',
    ];
}
{% endhighlight %}

No formRequest existe um método chamado `validated()` que devolve um 
array com os dados validados.
Vamos invocar o LivroRequest no nosso controller e deixar os
métodos store e update mais simplificados:

{% highlight php %}
use App\Http\Requests\LivroRequest;
...
public function store(LivroRequest $request)
{
    $validated = $request->validated();
    $livro = Livro::create($validated);
    request()->session()->flash('alert-info','Livro cadastrado com sucesso')
    return redirect("/livros/{$livro->id}");
}

public function update(Request $request, Livro $livro)
{
    $validated = $request->validated();
    $livro->update($validated);
    request()->session()->flash('alert-info','Livro atualizado com sucesso')
    return redirect("/livros/{$livro->id}");
}
{% endhighlight %}

### 3.5: Exercício FormRequest

- Implementação do FormRequest `LivroFulanoRequest`, onde `Fulano` é um identificador
seu.


