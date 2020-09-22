## Migrations

Criando uma migration que alterará uma tabela existente:
{% highlight bash %}
php artisan make:migration change_editora_colunm_in_livros  --table=livros
{% endhighlight %}

Alterando a coluna `editora` de string para text na migration acima:
{% highlight php %}
$table->text('editora')->change();
{% endhighlight %}


## Autenticação


## Autorização


## Rotas

Exemplos de rotas do tipo GET:
{% highlight php %}
Route::get('/livros/create','LivroController@create');
Route::get('/livros/{isbn}','LivroController@show');
{% endhighlight %}

Exemplos com REGEX. O primeiro só aceita número inteiro no parâmetro id,
o segundo somente letras em title e o terceiro combina os dois anteriores:
{% highlight php %}
Route::get('/livros/{id}','LivroController@show')->where('id','[0-9]+');
Route::get('/livros/{title}','LivroController@show')->->where('title','[A-Za-z]+');
Route::get('/livros/{id}/{title}','LivroController@show')->->where(['id' => '[0-9]+','title' => '[A-Za-z]+']);
{% endhighlight %}

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




{% endraw %}
{% endhighlight %}


## Rota assinada

## Bibliotecas gerais
### Gerador de fakers
### Biblioteca para PDF
### Biblioteca para Excel


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

 ## Bibliotecas USP - faltam alghumas

 Essa relação é exclusiva para quem trabalha na Universidade de São Paulo.

    composer require uspdev/senhaunica-socialite
    composer require uspdev/laravel-usp-validators
    composer require uspdev/replicado
    composer require uspdev/laravel-usp-theme
    composer require uspdev/laravel-usp-faker --dev
    

## tabebas pivot:
https://github.com/laracasts/Laravel-5-Generators-Extended/


use Illuminate\Validation\Rule;
['required', Rule::in($item::tipo_aquisicao)],


