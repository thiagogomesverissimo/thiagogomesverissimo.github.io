git tag -a v1.1 -m 'v1.1' --sign --local-user AAA3BE9F


-Essas entradas são adicionadas no /home/user/.gitconfig 
    git config --global user.name "Thiago"
 git config --global user.email "mail@gmail.com"
 git config --global color.ui auto
 git config --global color.interactive auto

-seção [alias]
 git config --global alias.a 'add'
 git config --global alias.s 'status'
 git config --global alias.aa '!add -A && status'
 git config --global alias.c 'commit'
 git config --global alias.cm 'commit -m'
 git config --global alias.co 'checkout'
 git config --global alias.f 'fetch'
 git config --global alias.p 'pull'
 git config --global alias.m 'merge'

-Sem linha pela metade
 git config --global core.pager less -r
 git config --global alias.d 'diff --color-words'

-logs
 git config --global alias.l "log --graph --pretty=format:'%C(yellow)%h%C(cyan)%d%Creset %s %C(white)- %an, %ar%Creset'"
 git config --global alias.ll 'log --stat --abbrev-commit'


#meld
 apt-get install meld
 -copiar para /usr/local/bin e dar permissao de escrita
 meld "$2" "$5" > /dev/null 2>&1
 git config --global diff.external '/usr/local/bin/git-diff.sh'

## Comandos do dia-a-dia

  - Add files for next commit
   git add . 

 -Cria um novo branch clonando o branch atual
   git checkout -b nova_branch 

 -Apagar branch
   git branch -D nova-branch

 - Apaga branch remotamente:
   git push origin --delete nome-branch 

 - apagar um commit:
   git rebase -p --onto 070b4e70f6d96ad^ 070b4e70f6d96ad
   git rebase --continue

 -Listar branchs
   git branch -a

 -Trocar de branch
   git checkout master

 -Voltar para última versão comitada, se você ainda não rodou 'git add'
   git checkout -- arquivo.txt 

 -Voltar para última versão comitada no caso de já ter rodado git add
   git reset HEAD arquivo.txt 

 -Estados da branch
   Antes do 'git add': file system
   Depois do 'git add': stage
   Depois do 'git commit': persistido
 -Usa-se o reset para mudar entre os estados

 -HEAD: última versão persistida

 -HEAD^: reverte as mudanças do último commit e coloca no file system (ou stage?)
   git reset HEAD^ 
   git reset --hard HEAD^

 -Depois tem que dar o  checkout para cada aquivo, ou:
 -Tira tudo que está em stage e manda para filesystem
   git reset HEAD . 
   git checkout -b fs/login
 -Enviar todas branchs
   git push -all

 -Acessar branch fs/login e atualizá-la a partir da branch master 
   git checkout fs/login 
   git merge master

 #Apagar branch do servidor remoto(origin):
  git push origin --delete minhabranch

-Tags: label para fazer realease de software
  git tag -a "1.0" -m "Versão Lançamento 1.0"
  git show-ref --tags
  git tag -l -n1
  git push --tags

-Branch push e pull
  git push origin branch-local:branch-remota
  git pull origin minha_branch

-Conflitos
 -Mante o nosso e descarta o remoto
   git checkout --ours 
 -Mante o remoto e descarta o local
   git checkout --theirs 

-Rastrea a branch remota
  git --set-upstream-to=origin/dev dev


-Boas práticas
 -Toda feature branch criamos a partir do branch dev
 -hotfix a partir do master (para bugfix)
 -As Tags cria no master


Revertendo mudanças se nada foi comitado:
    
    git checkout .

Revertendo mudanças se teve commit e desprezendo portanto o último commit:

    git revert HEAD
