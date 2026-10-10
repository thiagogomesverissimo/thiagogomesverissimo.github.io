---
title: 'Webform Pdf Drupal'
date: 2020-12-16
---

O módulo webform no Drupal tem um submódulo para geração de pdf fantástico
e que podemos customizar usando twig. Mas as vezes é difícil lembrar da syntax
da combinação dessas ferramentas, assim, deixo trechos de códigos que uso com
frequência.

<ul id="toc"></ul>

## Lista de links para arquivos

Suponha um campo chamado `arquivos` com múltiplos uploads. A função 
`webform_token('[webform_submission:values:arquivos]', webform_submission, [], options)` devolve uma string gigantesca com as urls de todos arquivos separas por `-`.
Com a função `split('-')` do twig dividimos essa string e conseguimos então iterar,
para fazemos o que quisermos com cada item da lista. Assim, podemos fazer algo como:

```php
{% raw %}
{% set arquivos = webform_token('[webform_submission:values:arquivos]', webform_submission, [], options) |split('-') %}

{% for i in arquivos %}
    <a href="{{i}}">{{  i|split('/')|last }} </a>
{% endfor %}
{% endraw %}
```

## Trabalhando com datas

Data de submissão do formulário em formato brasileiro:
```php
{% raw %}
{{ created |date("d/m/Y") }}
{% endraw %}
```


Mostrar a soma dos itens composite no webform

```php
{% raw %}
 {% for item in data.somacomposite %}
      {% set sum = item.somac + sum ?? 0 %}
  {% if loop.last %}{{ sum }}{% endif %}
 {% endfor %}
{% endraw %}
```
