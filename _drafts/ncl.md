Esses blocos de comando *ncl* são lembretes para mim mesmo. Grande parte desse material foi copiado <mateus teixeira>, com alguma modificações, sempre para deixar cada bloco o mais reprodutível possível.

Instalação usando binário e shell tipo bash:
 
 1. Fazer download do binário para seu sistema operacional, arquitetura e versão do gcc. Esses comandos te ajudarão: uname -s; uname -m; gcc -v. 
 2. Ao descompactar o arquivo baixado, serão criadas as pastas: bin, lib e include.
 3. mkdir -p $HOME/usr/ncarg
 4. cp -a lib bin include $HOME/usr/ncarg/
 5. Inserir no final do arquivo $HOME/.bashrc:
	
		NCARG_ROOT=$HOME/usr/ncarg
		PATH=$NCARG_ROOT/bin:$PATH
		export NCARG_ROOT PATH

ln -s /lib/x86_64-linux-gnu/libssl.so.1.0.0   /lib/x86_64-linux-gnu/libssl.so.0.9.8

apt-get install libssh2-1

sudo apt-get install libssl0.9.8:i386

sudo apt-get install libssl0.9.8
	
 6. opcional: wget http://www.ncl.ucar.edu/Document/Graphics/hluresfile  -O $HOME/.hluresfile

Criação de *array* e matrizes:

	;Rodar comandos no prompt do NCL
	ncl> vetor=(/10,12,14/)
	ncl> matriz=(/ (/10,12,14/), (/13,16,10/) /) ;Matriz 2x3
	;Matriz 2x3 com elementos igual a -999:
	ncl> matriz_nula=new( (/2,3/),integer,-999)
	
Prints comuns:

	ncl> numero=1.23456789
	ncl> print(sprintf("%10.2f",numero))
	ncl> print(sprintf("%10.2E",numero))
	ncl> print(sprintf("%10.2g",numero))
	ncl> print(sprintf("%10.2G",numero))


*Scripts*: É possível fragmentar o código em vários arquivos com extensão ncl. Para carregar um arquivo ncl dentro de outro:
	
	;pi.ncl
	begin
		pi=3.14
	end
	
	;main.ncl
	load "pi.ncl"
	begin
		print("Carregando outro arquivo NCL: ")
		print(pi)
	end
	$ ncl main.ncl

O sinal + é usado para concatenação:
	
	ncl> nome = "Jack"
	ncl> print(nome + " precisa de R$ " + 2.3)
	
Conversões entre tipos de variáveis:

	ncl> pi = 3.14
	ncl> print(typeof(pi))
	ncl> print(floattointeger(pi))

Atributos das variáveis, um dos tipos de meta-dados:
		
	ncl> y = (/ (/1,2,3/),(/2,3,4/) /)
	ncl> y@unidade = "ug/m3"
	ncl> y@responsavel = "joao"
	ncl> print(y)

Deletendo variáveis ou atríbutos:

	ncl> pi = 3.14
	ncl> pi@metodo = "Valor aproximado de pi em um experimento escolar"
	ncl> list_vars() ;Listar variáveis na memória RAM
	ncl> delete(pi@metodo) ; Deleta somente o atríbuto
	ncl> delete(pi) ; Deleta a variável
	
Os loops e condicionais são parecidos com fortran e é possível usar *break* e *continue*:
	
	;Exemplo do início,fim,incremento
	do i=1,10,1
		print("i=" + 1)
	end do
	
	;igual anterior, mas usando while. .le. menor ou igual à.
	i=1
	do while (i .le. 10)
		print("i=" + i)
		i=i+1
	end do
	
	;Exemplo de if:
	i=1
	j=1
	if (i .eq. j and i .gt. 100) then
		print("i e j sao iguais e i eh maior que 100")
	else
		print("nenhum condicao satisfeita")
	end if

Indexação de vetores e matrizes:
	
	ncl> vetor=(/1,2,3,4,5,6,7,8,9,10/)
	ncl> print(vetor(::)) ; é igual a: print(vetor)
	ncl> print(vetor(4:4)) ;é igual a: print(4) 
	ncl> print(vetor(2:8:2)) ; saida: 3,5,7,9
	
Indexação por coordenadas (não entendi muito bem...):
	
	ncl> temperaturas=(/10,11,12,13,14,15/)
	ncl> temperatura!0="lat" ;Nomenado dimensão
	ncl> temperaturas&lat=(/-10,-20,-30,-40,-50,-60/)
	ncl> print(temperaturas({-30})) ;é igual a:	print(temperaturas(2))
	
Manipulando os arquivos de dados. Exemplo usando dados de: <br> 
http://www.esrl.noaa.gov/psd/data/gridded/data.kaplan_sst.html
	
	;Lendo arquivo netcdf localmente	
	$ wget ftp://ftp.cdc.noaa.gov/Datasets/kaplan_sst/sst.mon.anom.nc 
	;r (leitura), c(criação), w (escrita/edição): 
	ncl> sst.mon.anom = addfile("sst.mon.anom.nc","r") 
	ncl> print(sst.mon.anom)
	
	;É possível baixar arquivo remotamente usando openDAP:
	ncl> url="http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/kaplan_sst/sst.mon.anom.nc"
	ncl> sst.mon.anom=addfile(url,"r")
	
	;importar dados da variável sst dentro do arquivo sst.mon.anom para a variável onlysst:
	ncl> onlysst=sst.mon.anom->sst
	
	;abrindo múltiplos arquivos, interessante para agregar outputs de simulação:
	;NÃO TESTEI AINDA
	ncl> arquivos = systemfunc("ls *.nc")
	ncl> todos = addfiles(arquivos,"r")
	ncl> pressao = todos[:]->pressao ;Pega a variável pressão de todos arquivos abertos
	
Operações matemáticas:

	;operação elemento a elemento
		ncl> A = (/1,2,3/)
		ncl> B = (/4,3,2/)
		ncl> print(A+B)
		ncl> print(A-B)
		ncl> print(A*B)
		ncl> print(2*A)
	
Trabalhando com dados ASCII:

	;Suponha o seguinte arquivo dados.txt :
	;separação das colunas usando TAB.
	1 2
	4 5
	7 8
	
	;Lendo como matriz:
	ncl> matriz<-asciiread("dados.txt",(/3,2/),"integer")
	
	;Lendo sequencialmente (e não como matriz):
	ncl> matriz<-asciiread("dados.txt",-1,"integer")
	
	;A função write_matrix mostra uma matriz formatada na tela:
	ncl> dados=(/ (/1,2/),(/3,4/) /)
	ncl> write_matrix(dados,"2i2",False) ; 2i2 é a dimensão

	;Mas podemos usá-la para escrever um arquivo ASCII:
	ncl> opcoes=True
	ncl> opcoes@fout = "saida_dados.txt"
	ncl> write_matrix(dados,"2i2",opcoes)
	
Criando arquivos netCDF:

	;metodo1.ncl
	begin
		meuNC=addfile("meunc.nc","c")
		dados=(/ (/1,2/),(/3,4/) /)
		meuNC->colunaExemplo=dados
	end
	
	;metodo2.ncl:
	begin
		meuNC=addfile("meunc.nc","c")

		;Atributos globais do arquivo
		fileAtt=True
		fileAtt@title="Meu netCDF"
		fileAtt@Conventions="None"
		fileAtt@creation_date = systemfunc("date")
		fileattdef(meuNC,fileAtt)

		;Dados
		dados=(/ (/1,2/),(/3,4/) /)
		dados@info="dados bacanas"
		;dimNomes-dimTamanho-dimIlimitadas:
		filedimdef(meuNC, (/"dados"/),-1, (/True/))
		filevardef(meuNC,"dados","integer","dados")
		filevarattdef(meuNC,"dados",dados)
		meuNC->colunaExemplo=(/dados/)
		print(dados)
		print(meuNC->colunaExemplo)
	end
	
Conversões entre os arquivos de dados:
		
	;grib para netcdf
	$ ncl_convert2nc teste.grb 
	
	;grib para netcdf usando CDO
	$ cdo -f nc copy teste.grb saida.nc
	
É possível executar códigos externos no ncl. Alguns exemplos com fortran são apresentados abaixo. 
**Exemplos com Fortran 77**:
	
	;Passo 1: criar uma rotina em fortran 77:
		;media.f
		C NCLFORTSTART
    	subroutine media(n1,n2,m)
    	real n1,n2,m
		C NCLEND
    	m = (n1+n2)/2.0
    	return
    	end

	;Passo 2: criar *shared object*, media.so:
		ncl> WRAPIT media.f 

	;Passo 3: usando rotina no script ncl:
		ncl> external MEDIA "./media.so"
		ncl> m=0.0
		ncl> MEDIA::media(2.0,1.0,m)
		ncl> print(m)
	
Exemplo usando fortran 90:
	
	;Passo 1: criar uma rotina em fortran 90:
		;media.f90
    	subroutine media(n1,n2,m)
				implicit none
				real, intent(in) :: n1,n2
				real, intent(out) :: m
    		m = (n1+n2)/2.0
    		return
    	end subroutine media

	;Passo 2: criar arquivo *stub*, media.stub:
		C NCLFORTSTART
    	subroutine media(n1,n2,m)
    	real n1,n2,m
		C NCLEND

	;Passo 3: criar *shared object*, media.so:
		ncl> WRAPIT media.stub media.f90

	;Passo 4: usando rotina no script ncl:
		ncl> external MEDIA "./media.so"
		ncl> m=0.0
		ncl> MEDIA::media(2.0,1.0,m)
	
Gráficos. Curiosidades, gsn significa Getting Started with NCL.
	
	;Gráfico de exemplo bidimensional XY:
	ncl> dados = random_uniform(-10,10,100)
	ncl> wks = gsn_open_wks("x11","exemplo");wks=workstation
	ncl> plot_dados = gsn_csm_y(wks,dados,False)
	
	;mesmo exemplo anterior, mas salvando um arquivo exemplo.ps:
	ncl> dados = random_uniform(-10,10,100)
	ncl> wks = gsn_open_wks("ps","exemplo");x11,ps,eps,pdf
	ncl> plot_dados = gsn_csm_y(wks,dados,False)
	$ evince exemplo.ps
		
	;mesmo exemplo anterior, mas com recursos no gráfico (título,eixos...):
	;exemplo_grafico.ncl
		begin
			dados = random_uniform(-10,10,100)
			recursos=True
			recursos@tiMainString="Grafico exemplo"
			recursos@tiXAxisString="nome do Eixo X"
			recursos@tiYAxisString="nome do Eixo Y"
			recursos@gsnMaximize=True ;Usar pagina inteira
			wks = gsn_open_wks("pdf","exemplo");x11,ps,eps,pdf
			plot_dados = gsn_csm_y(wks,dados,recursos)
		end
	$ ncl exemplo_grafico.ncl 

Referências:
 
 - http://www.ncl.ucar.edu/
 - http://www.ncl.ucar.edu/Document/Functions/list_alpha.shtml
 - http://www.ncl.ucar.edu/Training/
 - http://www.ncl.ucar.edu/Training/Workshops/index.shtml
 - http://www.ncl.ucar.edu/Training/Workshops/Scripts/
