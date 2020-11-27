---
title: 'Click event: javascript or jquery'
date: 2020-11-17
permalink: /posts/click-event-javascript-or-jquery
categories:
  - jquery
tags:
  - jquery
---

Sabe aquele momento que paramos e pensamos: Faço essa implementação
com `javascript` ou `Jquery`? Segue uma implementação de um link 
chamado `Adicionar Item` que toda vez que é clicado adiciona um
item sequencial numa lista. Posto aqui para simples reflexão...

Implementação com `javascript`:
{% highlight html %}
{% raw %}
<!DOCTYPE html>
<body>
  <a href="#" onclick="add();return false;">Adicionar Item</a>
  <ul id="lista"></ul>
  <script>
    i = 1;
    function add(){
      var x = document.createElement('li');
      x.innerHTML = "elemento " + i;
      document.getElementById('lista').appendChild(x);
      i++;
    }
  </script>
</body>
</html>
{% endraw %}
{% endhighlight %}

Implementação com `Jquery`:
{% highlight html %}
{% raw %}
<!DOCTYPE html>
<body>
  <a href="#" id="add">Adicionar Item</a>
  <ul id="lista"></ul>
  <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>   
  <script>
    i = 1;
    $(document).ready(function(){
      $('#add').on('click',function(){
        $('#lista').append('<li>elemento ' + i +'</li>');
        i++;
      });
    });
  </script>
</body>
</html>
{% endraw %}
{% endhighlight %}