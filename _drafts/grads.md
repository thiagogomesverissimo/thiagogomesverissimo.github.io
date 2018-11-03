Grads
=====
#Site da NOAA para baixar arquivos *.nc: http://www.esrl.noaa.gov/psd/data/gridded/data.noaa.oisst.v2.html

São necessário 2 arquivos: dados.dat e descritor.ctl, onde o descritor.ctl descreve as dimensões dos dados. 

#Exemplo do descritor.ctl (dados com 4 dimensões):
 DSET vento.dat
 TITLE Dados de  vento
 UNDEF -99999 #ignorados na plotagem
 XDEF 80 LINEAR -140.0 1.0 #80 pontos na direção x,longitude inicial: -140, espaçemento em pontos de grade: 1.0 
 YDEF 50 LINEAR   20.0 1.0 #50 pontos na direção y,latitude inicial: 20, espaçemento em pontos de grade: 1.0
 ZDEF 5 LINEAR 1000 850 500 300 100 #5 níveis verticais, onde 1000 850 500 300 100 são os cinco níveis.
 TDEF 4 LINEAR 0Z10apr1991 12hr #4 tempos, tempo inicial: 0Z10apr1991, varia de 12h em 12h.
 VARS 2
 u 5 0 componente u do vento #5 níveis da variável v, 0 é o código de unidade
 v 5 0 componente v do vento
 ENDVARS

#Mudando a cor de fundo do grads
 ga> set display color white
 ga> clear

#Grads em modo bach
 $ grads -b
 
#Rodando grads do terminal
 $ grads -c "meu comando grads"

#Abrindo ctl
 ga> open /home/thiago/model.ctl #primeiro arquivo descritor
 ga> query file 1 #Mostar info do primeiro arquivo descritor
 ga> query dims 1
 ga> display minhavariavel
 ga> display u,v #Plotando duas variáveis simultaneamente

#Fecha todos ctls abertos
 ga> reinit 

#Roda comando do terminal: !
 ga>!ls
 
#plotando, fazer set do lat antes do lon:
 ga> set time 02JAN1987 09JAN1987 #quando 
 ga> set lat -20 -10 #onde, poderíamos usar set y. Lembrar: grads considera variação Y de sul->norte
 ga> set lon -80 -20 #poderíamos usar set x. Lembrar: grads considera variação X de oeste->leste
 da> set gxout line #como
 
#Plotando vento u brasil
 ga> set mpdset hires brmap # o que faz?
 ga> query dims
 ga> set lat -35 5
 ga> set lon -75 -30
 ga> display v
 ga> display skip(u,5);v

#Perfil vertical de temperatura em Belém do Pará
 ga> set lat -1.5
 ga> set lon -48
 ga> set z 1 7
 ga> set zlog on
 ga> display tair #tair é nome da variável de temperatura

#Perfil vertical zonal de velocidade potencial ao longo da faixa equatorial (secção longitudeXaltitude)
 ga> set lat 0
 ga> set z 1 7
 ga> set zlog on
 ga> display tair

#Usando a opção gxout, de tipo de gráfico:
 ga> set mpdset hires brmap
 ga> set gxout contour # outras opções: shaded,grfill,grid,vector,stream,barb,bar,line,scatter
 ga> display tair

#Mostra estatísticas:
 ga> set mpdset hires brmap
 ga> set stat
 ga> display tair

#Para fazer animação, basta especificar intervalo de tempo:
 ga> set T jan1990 jun1990
 ga> set T 1 last #engloba todo tempo disponível

#Projeções
 ga> set map 1 1 10
 ga> set mproj scaled #Outras opções: scaled,sps,robinson,mollweide,lambert,off,
 ga> display p #p: precipitação

#Inserindo textos nos gráficos:
 ga> draw title ventos horizontais 
 ga> draw xlab Longitude
 ga> draw ylab Latitude
 ga> draw string 10 10 Meu texto #Escreve "Meu texto" na posição 10 10
 ga> draw line x1 y1 x2 y2 # linha do ponto 1 ao 2

#Pegar coordenadas ao clicar no Gráfico:
 ga> query pos
 ga> ll2xy lon lat
 
#Remove logotipo grads:
 ga> set grads off

#Impressão
 ga> set parea xmin xmax ymin ymax
 ga> set parea off

#Salvando arquivo .gmf
 ga> enable print meuarquivo.gmf
 ga> display tair
 ga> print
 ga> disable print

#Visualizando arquivos .gmf com gxtran
 ga> !gxtran -a -g 800x600 -i meuarquivo.gml

#Convertendo arquivos .gmf para .ps:
 $ gxps -c -i teste.gmf -o arquivo.ps
 #Ou:
 $ gxeps -c -a -i teste.gmf -o arquivo.eps 

#Salvando em png/jpg:
 ga> display tair
 ga> printim teste.png white

#Scripts gs para grads:
 *Essa linha é um comentário
 'open exemplo.ctl'
 'display tair'

#rodando scripts de dentro do grads:
 ga> run meuarquivo.gs #linhas com apóstrofos
 ga> exec meuarquivo.gs #linhas sem apóstrofos

#Exemplo de script, dado o arquivo.gs:
 *Meu primeiro script grads
 'open /home/thiago/model.ctl'
 'display tair'
 'printim tair.png white'
 #Abrindo no grads
 ga> run arquivo.gs

#Carregar opções de gráficos antes de displays:
 ga> set imprun meuarquivo
 ga> display tair

#Programando
 ga> say 'Iniciando plotagens'
 ga> prompt 'Digite a latitude'
 ga> pull minlat maxlat
 ga> set lat 'minlat%' '%maxlat'

#Abrindo arquivo de dados sem descriptor(sdf: self-describe-file):
 ga> sdfopen meuarquivo.nc 
