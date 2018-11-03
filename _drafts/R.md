# compilar R

apt-get install f2c g++ gfortran gcc
sudo apt-get install build-essential
sudo apt-get install fort77
sudo apt-get install xorg-dev #Esse precisa mesmo
sudo apt-get install liblzma-dev  libblas-dev gfortran
sudo apt-get install gcc-multilib
sudo apt-get install gobjc++
sudo apt-get install aptitude
sudo aptitude install libreadline-dev

./configure --prefix=/home/thiago/compilados/R --with-x=no
./configure --prefix=/home/thiago/compilados/R --x-includes=/usr/include/X11/ --x-libraries=/usr/lib/X11/
make 
make check

export PATH=$PATH:/home/thiago/compilados/R/bin
which R

#Não tenho certeza:
export LD_LIBRARY_PATH=~/local/lib
export C_INCLUDE_PATH=~/local/include 

Instalação via repositótios: http://www.jason-french.com/blog/2013/03/11/installing-r-in-linux/

Libcurl:
sudo apt-get install libcurl4-openssl-dev
Se quiser compilar curl e libcurl: http://curl.haxx.se/download.html

## Gerenciamento de pacotes
.libPaths(c(.libPaths(),"/home/thiago/remota"))

install.packages("zoo", lib="C:/software/Rpackages")
library("zoo", lib.loc="C:/software/Rpackages")


Matriz
linhas=2
colunas=2
m=matrix(c(1,2,3,4),linhas,colunas,byrow=TRUE)
dim(m)


# No Ubuntu Trusty

#Método 1
sudo apt-get install gcc-multilib
sudo apt-get install gobjc++
sudo apt-get install liblzma-dev libblas-dev gfortran
sudo apt-get install fort77
sudo apt-get install build-essential
apt-get install f2c g++ gfortran gcc
sudo apt-get install xorg-dev #Esse precisa mesmo
sudo apt-get install aptitude
sudo aptitude install libreadline-dev
sudo apt-get install zlib-bin lzma

# Método 2:
  apt-get build-dep r-base

wget http://cran-r.c3sl.ufpr.br/src/base/R-3/R-3.2.0.tar.gz
./configure --prefix=/home/thiago/compilados/R-3.0.2 --x-includes=/usr/include/X11 --x-libraries=/usr/lib/X11 --enable-R-shlib
make
make install

export PATH="/home/thiago/compilados/R/bin:$PATH"
which R

export RSTUDIO_WHICH_R=/home/thiago/compilados/R-3.0.2/bin/R
#export R_HOME="/usr/lib/R"

# Gerenciamento de pacotes
.libPaths(c(.libPaths(),"/home/thiago/R/local"))

install.packages("zoo", lib="/home/thiago/R/local")
library("zoo", lib.loc="/home/thiago/local")



