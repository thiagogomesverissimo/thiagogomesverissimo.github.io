---
title: 'Gerando animação com gource para todos repositórios de uma organização do github'
date: 2019-12-30
permalink: /posts/gource-organization
categories: 
  - tutorial
tags:
  - gource
  - git 
---
O gource é um software que nos permite, dentre outras coisas,
gerar uma animação gráfica e bonita da linha do tempo dos commits 
de um projeto no git. Vou mostrar como usá-lo em um cenário no qual
queremos gerar uma animação para todos repositórios de uma dada
organização no github.

Primeiramente, instale o gource:

{% highlight bash %}
sudo apt install gource
{% endhighlight %}

Se preferir compilar, para usar opções mais recentes, instale as
dependências:

{% highlight bash %}
sudo apt install libsdl2-dev libsdl2-image-dev \
libfreetype6-dev libglew-dev libglm-dev libpcre3-dev \
libboost-filesystem-dev libpng-dev libtinyxml-dev
{% endhighlight %}

E depois compile:

{% highlight bash %}
git clone https://github.com/acaudwell/Gource.git
cd Gource
./autogen.sh
./configure
make
sudo make install
{% endhighlight %}

Para listar todos repositórios de sua organização, 
gere um token no github e coloque numa variável do bash. 
Também crie uma variável com o nome da sua organização do github: 

{% highlight bash %}
token='blabla'
org='uspdev'
{% endhighlight %}

Faça uma requisição GET para trazer um arquivo json com 
informações dos projetos na organização:

{% highlight bash %}
repos=$(curl -s -H "Authorization: token $token" "https://api.github.com/orgs/$org/repos?per_page=100")
{% endhighlight %}

Vamos filtrar somente os nomes dos repositórios:

{% highlight bash %}
repos=$(echo $repos | grep full_name | cut -f2 -d:)
repos=$(echo $repos | sed -r 's/"| |,//g')
repos=$(echo $repos | tr '\n' ' ')
echo $repos
{% endhighlight %}

Agora com a variável *$repos* conseguimos clonar todos 
repositórios:

{% highlight bash %}
mkdir $org
cd $org
for repo in ${(z)repos}; do git clone git@github.com:$repo.git; done
{% endhighlight %}

Com o *gource* vamos gerar um arquivo com histórico 
dos commits de todos repositórios: 

{% highlight bash %}
for i in $(ls); do gource --output-custom-log $i.txt $i ; done
cat *.txt | sort -n > uspdev.txt
{% endhighlight %}

Neste ponto já é possível vizualizar uma animação básica:

{% highlight bash %}
gource uspdev.txt
{% endhighlight %}

Entretanto, vou fazer algumas modificações para deixar 
o vídeo mais agradável. Primeiramente, com o comando abaixo, 
olhe  a lista de autores(as) dos commits, perceba que a mesma
pessoa as vezes usa nomes diferentes em cada commit.

{% highlight bash %}
cat uspdev.txt| cut -d'|' -f2| sort| uniq
{% endhighlight %}

Com o *sed* é possível fazer as correções. Eu
vou substituir os nomes das pessoas pelos nomes
dos respectivos locais de trabalho, 
exemplos de algumas substituições:

{% highlight bash %}
sed -i "s/Thiago Gomes Verissimo/FFLCH/g" uspdev.txt
sed -i "s/Marcelo Modesto Costa/IME/g" uspdev.txt
sed -i "s/Sybele Groff/IF/g" uspdev.txt
sed -i "s/Tadeu Mesquita/FDRP/g" uspdev.txt
sed -i "s/Priscila C. Alves/EE/g" uspdev.txt
sed -i "s/milton brasileiro/IB/g" uspdev.txt
sed -i "s/Alessandro Costa de Oliveira/ECA/g" uspdev.txt
sed -i "s/Masaki Kawabata Neto/EESC/g" uspdev.txt
sed -i "s/André Girol/DF-FFCLRP/g" uspdev.txt
sed -i "s/Erickson Zanon/IGC/g" uspdev.txt
sed -i "s/Fabiana M. Munhoz Rodrigues/ICB/g" uspdev.txt
sed -i "s/Lucas Flóro/FEARP/g" uspdev.txt
sed -i "s/Igor Vitorio Custodio/ICMC/g" uspdev.txt
sed -i "s/Pascoal Roberto Peduto/FSP/g" uspdev.txt
sed -i "s/Lucas Flóro/FEARP/g" uspdev.txt
sed -i "s/João Paulo Polles/EXTERNO/g" uspdev.txt
{% endhighlight %}

Vou deletar alguns commits que não consegui identificar 
exatamente o(a) autor(a):

{% highlight bash %}
sed -i '/root/d' uspdev.txt
sed -i '/joazinho/d' uspdev.txt
{% endhighlight %}

Se quiser, é possível verificar a quantidade de commits 
por local:

{% highlight bash %}
cat uspdev.txt| cut -d'|' -f2| sort| uniq -c | sort -nr
{% endhighlight %}

Crie um diretório *~/logos* com as imagens de cada local
com extensão .jpg.

Agora podemos gerar a animação, com algumas opções
extras deixando-a mais agradável:

{% highlight bash %}
gource --title "Contribuições USPdev 2018-2019" \
    --fullscreen                                 \
    --date-format "%d/%m/%Y %H:%M:%S"            \
    --start-date '2018-01-01'                    \ 
    --user-image-dir ~/logos                     \
    --logo ~/logos/USPDEV.png                    \
    --seconds-per-day 0.3                        \
    --max-user-speed 30                          \
    --font-colour 098735                         \
    --max-files 200                              \
    --user-scale 1.7                             \
    --font-scale 1.1                             \
    --font-size 30                               \
    --user-font-size 45                          \
    --highlight-users                            \
    --highlight-colour 026AA7                    \
     uspdev.txt
{% endhighlight %}

Para exportar o arquivo como *mp4*, instale o *ffmpeg*:

{% highlight bash %}
sudo apt install ffmpeg
{% endhighlight %}

E no comando acima do *gource* acrescente no final:

{% highlight bash %}
-1280x720 -o - | ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i - -vcodec libx264 -preset ultrafast -pix_fmt yuv420p -crf 1 -threads 0 -bf 0 gource.mp4
{% endhighlight %}

Resultado:
<iframe width="560" height="315" src="https://www.youtube.com/embed/3KTLhKROza8" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
