---
title: 'truques shell script'
date: 2019-03-11
permalink: /posts/truques-shell-script
tags:
  - shell
---


Cabeçalho
  #!/bin/bash

Pegar horário atual:
  agora=$(date -d 'today' '+%Y.%m.%d.%H.%M.%S')

Exemplo de if (gt: maior que):
  if [ 2 -gt 1 ]; then
    echo 'Ola';
  fi

  if [ 2 -gt 1 ]; then
    echo 'Ola';
  fi
  elif [2 -gt 3]; then
    echo "eu de novo"
  elif [2 -gt 4]; then
    echo "eu de novo"
  else 
    echo "ixi"
  fi 

Exemplo de for:
  for i in *; do 
    echo "$i é um arquivo bacana"; 
  done

  for i in `ls`; do 
    echo "$i é um arquivo bacana"; 
  done

verifica se o arquivo especificado existe:
  if [ -e "dns.txt" ]; then 
    echo "The file dns.txt exists"; 
  fi

Exemplo usando Interface:
  zenity --info --text "ola mundo"

# echo mesma linha

    for i in $(ls); do echo -n "$i, "; done

# resolve problema do sepador de lista ser o espaço no for:

    IFS=$'\n'
    for i in $(ls); do echo $i; done

# Procura todos arquivos que tem a sequência 'abcd' e troca por '1234'

    for i in $(grep -r abcd * | cut -d':' -f1); do sed -i s/"abcd"/"1234"/g $i; done
    
# Procura e apaga:
 
    find ../../inputs/pmf/ -name "*.xls" -exec rm {} \;

Arquivos diferentes em dois diretórios:

    diff -rq dir1 dir2
