---
title: 'Tópicos em Laravel'
date: 2020-04-10
permalink: /posts/topicos-em-laravel
categories:
  - tutorial
tags:
  - laravel
---

Pequenos trechos de códigos em laravel usados com frequência, nada que substitua
a documentação oficial.

# Validação

Quando estamos dentro de um método do controller podemos usar *$this->validate*,
que validará os campos com a condições que passaremos e caso falhe a validação: 
1. automaticamente retornará o usuário para página de origem. 
2. Devolverá para página de origem os inputs enviados na requisição 
3. Enviará para página de origem as mensagens de erro da validação

{% highlight bash %}
$this->validade([$request,[
  'nome' => 'required'
]]);
{% endhighlight %}

Podemos também usar o classe Validator, neste caso temos que fazer o redirect
para a origem da requisição por nossa conta com os inputs e erros.

{% highlight bash %}
$validator = Validator::make($request->all(),[
  'nome' => 'required'
]);
if($validator->fails()){
  return redirect('/node/create')
          ->withErrors($validator)
          ->withInput();
}
{% endhighlight %}

# Arquivos

No formulário html:
{% highlight bash %}
<form method="POST" enctype="multipart/form-data">
  <input type="file" name="certificado">
</form>
{% endhighlight %}

No controller:
{% highlight bash %}
if($request->hasFile('certificado')){
  if($request->)
}
{% endhighlight %}
