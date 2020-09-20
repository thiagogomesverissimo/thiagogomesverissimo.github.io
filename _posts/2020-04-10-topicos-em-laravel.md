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

Vamos começar a espalhar mais o tratamento das requições em uma arquitetura
convencional?

Criando um controller:
{% highlight bash %}
php artisan make:controller LivroController
{% endhighlight %}
O arquivo criando está em `app/Http/Controllers/LivroController.php`.

Vamos criar um método chamado `index()` dentro do controller gerado:
{% highlight php %}
public function index(){
    return "Não há livros cadastrados nesses sistema ainda!";
}
{% endhighlight %}

Vamos alterar nossa rota para apontar para o método `index()`
do `LivroController`:

{% highlight php %}
Route::get('/livros', 'LivroController@index');
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
Route::get('/livros/{isbn}', 'LivroController@show');
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
    return view('livros.show')->with('livro',$livro);
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
deixando o autor como opicional.

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
Essa é uma da inúmeras convêncões que vamos nos deparar ao usar um framework.

Vamos modificar o controller para operar com os livros do banco de dados?
No método index vamos buscar todos livros no banco de dados e enviar para
o template:
{% highlight php %}
public function index(){
    $livros = App\Models\Livro:all();
    return view('livros.index')->with('livros',$livros);
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
    return view('livros.show')->with('livro',$livro);
}
{% endhighlight %}

No template vamos somente printar o livro:
{% highlight php %}
{% raw %}
<li>{{ $livro->titulo }}</li>
<li>{{ $livro->autor }}</li>
<li>{{ $livro->isbn }}</li>
{% endraw %}
{% endhighlight %}

### 1.5: Fakers

Durante o processo de desenvolvimento precisamos manipular dados
constantemente, então é uma boa ideia gerar dados aleatórios para
não termos que sempre criá-los manualmente:

{% highlight bash %}
php artisan make:factory LivroFactory --model='Livro'
{% endhighlight %}

{% highlight php %}
return [
    'titulo' => $this->faker->sentence(5),
    'isbn'   => $this->faker->ean13(),
    'autor'  => $this->faker->name
];
{% endhighlight %}

Em `database/seeders/DatabaseSeeder.php` vamos criar ao menos um registro
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

Agora, vamos zerar o banco e subir nossos dados fake:
{% highlight bash %}
php artisan migrate:fresh --seed
{% endhighlight %}

### 1.6: Exercícios MVC

- Implementação de um model chamado `LivroFulano`, onde `Fulano` é um identificador
seu. Implementar uma migration correspondente com os campos: titulo, autor e isbn.
- Implementar faker correspondente
- Implementar controller com os métodos index e show com respectivos templates e rotas

## 2. CRUD: Create (Criação), Read (Consulta), Update (Atualização) e Delete (Destruição)

Frameworks como o laravel são flexíveis o suficente para ser customizados ao seu gosto.
Porém, sou partidário da ideia de seguir convênções quando possível. Por isso começaremos
criando a estrututa básica para implementar um CRUD:

{% highlight bash %}
rm app/Models/Livro.php
rm app/Http/Controllers/LivroController.php
php artisan make:model LivroController -a
{% endhighlight %}
