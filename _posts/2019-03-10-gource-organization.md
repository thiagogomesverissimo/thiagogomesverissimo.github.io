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

1. Gerar lista com repositórios:

{% highlight bash %}
token='blabla'
org='uspdev'
repos=$(curl -s -H "Authorization: token $token" "https://api.github.com/orgs/$org/repos?per_page=100" | grep full_name | cut -f2 -d: | sed -r 's/"| |,//g')
{% endhighlight %}

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
