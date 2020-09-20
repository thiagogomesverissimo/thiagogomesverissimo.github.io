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


## 1. MVC - model view controller

### 1.1 Request e Response ou Pergunta e Resposta

Criando um projeto chamado `biblioteca` para nossos exemplos:
{% highlight bash %}
composer create-project laravel/laravel biblioteca
cd biblioteca
php artisan serve
{% endhighlight %}

Criando uma rota para recebimento das requisições.
{% highlight php %}
Route::get('/livros', function () {
    echo "Não há livros cadastrados nesses sistema ainda!";
});
{% endhighlight %}

### 1.2 Controller

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

### 1.3 View: Blade

Vamos melhorar os retornos do controller?
A principal caracteristica do sistema de template é a herança. Então, vamos
começar criando um template principal `resources/view/main.blade.php` 
com seções genéricas:

<!DOCTYPE html>
<html>
    <head>
        <title>@section('title') Exemplo @show</title>
    </head>
    <body>
        @yield('content')
    </body>
</html>

Primeiramente, vamos criar o template para o index `resources/views/livros/index.blade.php`:
obedecendo a estrutura:

@extends('main')
@section('content')
  Não há livros cadastrados nesse sistema ainda!
@endsection

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

@extends('main')
@section('content')
  {{ $livro }}
@endsection

## 2. CRUD: Create (Criação), Read (Consulta), Update (Atualização) e Delete (Destruição)

Frameworks como o laravel são flexíveis o suficente para ser customizados ao seu gosto.
Porém, sou partidário da ideia de seguir convênções quando possível. Por isso começaremos
criando a estrututa básica para implementar um CRUD:

{% highlight bash %}
rm app/Http/Controllers/LivroController.php
php artisan make:model LivroController -a
{% endhighlight %}
