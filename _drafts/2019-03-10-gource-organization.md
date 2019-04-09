---
title: 'Gerando animação com gource para todos repositórios de uma organização do github'
date: 2019-03-19
permalink: /posts/gource-organization
categories: 
  - tutorial
tags:
  - gource
  - git 
---

Instalação das depências necessárias para o gource:

    libsdl2-dev libsdl2-image-dev libpcre3-dev
    libfreetype6-dev libglew-dev libglm-dev
    libboost-filesystem-dev libpng12-dev libtinyxml-dev

Compile e instale do gource:

{% highlight bash %}

    # https://github.com/acaudwell/Gource/blob/master/INSTALL
    git clone https://github.com/acaudwell/Gource.git
    cd Gource
    ./configure
    make
    make install
    
{% endhighlight %}

Gerar token no github e salvar numa variável: 

{% highlight bash %}
token='blabla'
org='uspdev'
{% endhighlight %}
Montar lista com os repositório de uma organização:

{% highlight bash %}
repos=$(curl -s -H "Authorization: token $token" "https://api.github.com/orgs/$org/repos?per_page=100")
{% endhighlight %}

repos=$(echo $repos | grep full_name | cut -f2 -d:)

repos=$(echo $repos | sed -r 's/"| |,//g')
repos=$(echo $repos | tr '\n' ' ')

2. clonar todos repositórios

3. gerar arquivo de log

https://github.com/acaudwell/Gource/wiki/Visualizing-Multiple-Repositories

gource --output-custom-log log1.txt repo1
gource --output-custom-log log2.txt repo2
...
cat log1.txt log2.txt | sort -n > combined.txt

4. substituindo nomes

5. logos das unidade

6. vídeo

gource combined.txt
gource -1280x720 -o - | ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i - -vcodec libx264 -preset ultrafast -pix_fmt yuv420p -crf 1 -threads 0 -bf 0 gource.mp4
