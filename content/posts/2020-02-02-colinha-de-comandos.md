---
title: 'Minha colinha de comandos gnu/linux'
date: 2020-02-02
---

Segue-se minha colinha de comandos no gnu/linux, em especial no debian, para tarefas corriqueiras:

Configurar expiração de conta do usuário em uma data:
 
```bash
usermod -e "September 20, 2014" USUARIO
```

Compactando com tar.gz: 

```bash
tar -vzcf files.tar.gz /home/thiago/files
tar -vzjf files.tar.gz /home/thiago/files
```

Descompactar arquivo em bzip2:

```bash
tar -vjxf file.tar.bz2
```
 
Programar reboot daqui a seis horas: 

```bash
shutdown -r +6:00
```

Fazer usuário a trocar senha no próximo login:

```bash
chage -d 0 USUARIO
```  
    
Fazer usuário trocar de senha a cada 60 dias:

```bash
chage -M 60 bianca
```
    
Deletar usuário e home:
```bash
deluser thiago --remove-home
```

Reparando partição:

```bash
fsck.ext4 /dev/sda1
```
 
Remontar partição sem precisar reinicar:

```bash
mount -o remount rw /particao
```

Listagem de arquivos ordenada por tamanho:
```bash
ls -lS
```

Move diretório Desktop/mygits para repos? (não me lembor):
```bash
find . -type f -exec sed -i "s/Desktop\/mygits/repos/g" {} \;
```

Muda hostname sem precisar reiniciar:
```bash
hostnamectl set-hostname sti-035374
```

Teclado ABNT2:
```bash
setxkbmap -model abnt2 -layout br
```
