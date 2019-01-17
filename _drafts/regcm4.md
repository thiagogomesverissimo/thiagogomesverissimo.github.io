---
layout: single
title:  "Instalação do RegCM 4"
header:
  teaser: "unsplash-gallery-image-2-th.jpg"
categories: 
  - regcm
tags:
  - regcm
---

RegCM é um modelo de área limitada (LAM).

Para fazer a instalação das bibliotecas que o *RegCM* depende:

    export ROOT="/home/thiago"
ulimit -c unlimited

# Paths
export REGCM="$ROOT/compilados/regcm4"
export LIBRARIES="$ROOT/compilados/regcm4/LIBRARIES"
export DOWNLOADS="$ROOT/Downloads"

# Compiladores:
export CC=gcc       #"gcc -fPIC ou icc -fPIC"
export CXX=g++      #"g++ -fPIC ou icpc -fPIC"
export FC=gfortran  #"gfortran -fPIC ou ifort -fPIC"

# bibliotecas compiladas localmente:
export NETCDF="$LIBRARIES/netcdf"
export ZLIB="$LIBRARIES/zlib"
export SZIP="$LIBRARIES/szip"
export HDF5="$LIBRARIES/hdf5"
export OPENMPI="$LIBRARIES/openmpi"

    mkdir -p "$ROOT/compilados/regcm4/LIBRARIES"


    export regcm_version=4.4.1
    cd $DOWNLOADS
    wget http://gforge.ictp.it/gf/download/frsrelease/213/1371/RegCM-4.4.1.tar.gz
    tar -vzxf RegCM-$regcm_version.tar.gz
    cd RegCM-$regcm_version
    ./configure --with-netcdf=$NETCDF --with-hdf5=$HDF5 --with-szip=$SZIP --prefix=$REGCM
    make >& regcm.log
    make install

    

#!/bin/bash
#***********************************************
# Script de instalação das bibliotecas. 
# O script abaixo também instala as bibliotecas:
# RegCM-4.4.1/Tools/Scripts/prereq_install.sh
#*********************************************** 

#Sempre que rodar, conferir e atualizar as versões:
export zlib=1.2.8
export szip=2.1
export hdf5=1.8.15
export openmpi=1.8.4 #check URL too. 
export netcdf_c=4.3.3
export netcdf_f=4.4.2

#zlib
cd $DOWNLOADS
wget http://zlib.net/zlib-$zlib.tar.gz
tar -vzxf zlib-$zlib.tar.gz
cd zlib-$zlib
./configure --prefix=$ZLIB
make
#make check
make install

#szip
cd $DOWNLOADS
wget http://www.hdfgroup.org/ftp/lib-external/szip/$szip/src/szip-$szip.tar.gz
tar -vzxf szip-$szip.tar.gz
cd szip-$szip
./configure --prefix=$SZIP
make
#make check
make install

#hdf5
cd $DOWNLOADS
wget http://www.hdfgroup.org/ftp/HDF5/current/src/hdf5-$hdf5.tar.gz
tar -vzxf hdf5-$hdf5.tar.gz
cd hdf5-$hdf5
./configure --prefix=$HDF5 --enable-fortran --enable-cxx --with-szlib=$ZLIB
#./configure --prefix=$HDF5 --disable-fortran --disable-cxx --with-szlib=$ZLIB
make
#make check
make install
#make check-install

#NetCDF-C:
cd $DOWNLOADS
wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-$netcdf_c.tar.gz
tar -vzxf netcdf-$netcdf_c.tar.gz
cd netcdf-$netcdf_c
./configure --prefix=$NETCDF           \
  LDFLAGS="-L$ZLIB/lib -L$HDF5/lib"    \
  CPPFLAGS="-I$ZLIB/include -I$HDF5/include"
make
#make check
make install

#Interface NetCDF-fortran:
cd $DOWNLOADS
wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-fortran-$netcdf_f.tar.gz
tar -vzxf netcdf-fortran-$netcdf_f.tar.gz
cd netcdf-fortran-$netcdf_f
./configure --prefix=$NETCDF      \
  LDFLAGS="-L$ZLIB/lib -L$HDF5/lib -L$NETCDF/lib" \
  CPPFLAGS="-I$ZLIB/include -I$HDF5/include -I$NETCDF/include"
make
make install

#openmpi
cd $DOWNLOADS
wget http://www.open-mpi.org/software/ompi/v1.8/downloads/openmpi-$openmpi.tar.gz
tar -vzxf openmpi-$openmpi.tar.gz
cd openmpi-$openmpi
./configure --prefix=$OPENMPI --disable-cxx
make
make install

#./configure CC="$CC" FC="$FC" F77="$FC" CXX="$CXX" --prefix=$DEST --disable-cxx
#./configure CC="$CC" FC="$FC" F77="$FC" CXX="$CXX" --prefix=$DEST

Atualize seu bash: 

# Colocar executáveis no sistema operacional:
export PATH="$NETCDF/bin:$PATH"
export PATH="$OPENMPI/bin:$PATH"

# Bibliotecas do sistema:
export LD_LIBRARY_PATH="$NETCDF/lib:$LD_LIBRARY_PATH" 
export LD_LIBRARY_PATH="$OPENMPI/lib:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH="$HDF5/lib:$LD_LIBRARY_PATH" 
export LD_LIBRARY_PATH="$ZLIB/lib:$LD_LIBRARY_PATH" 

#flags
export CPPFLAGS="-I$HDF5/include -I$ZLIB/include -I$NETCDF/include"
export LDFLAGS="-L$HDF5/lib -L$ZLIB/lib -L$NETCDF/lib -lnetcdff -lnetcdf"

#Opicionais
export MPIFC="$OPENMPI/bin/mpif90"
export LIBS="-lnetcdff -lnetcdf -lhdf5_hl -lhdf5 -lz"}

Compilação RegCM
     
export regcm_version=4.4.1
cd $DOWNLOADS
wget http://gforge.ictp.it/gf/download/frsrelease/213/1371/RegCM-4.4.1.tar.gz
tar -vzxf RegCM-$regcm_version.tar.gz
cd RegCM-$regcm_version
./configure --with-netcdf=$NETCDF --with-hdf5=$HDF5 --with-szip=$SZIP --prefix=$REGCM
make >& regcm.log
make install

Será gerada uma pasta bin com os executáveis. 
Opicional: Se preferir deixar os comando disponíveis no sistema:
    
    ln -s $REGCM/bin/RegCM-4.4.1/bin/* /usr/local/bin/


Para definir o DOMAIN precisamos baixar dados de topografia, classificação de solo, profundidade de lagos e textura:

#!/bin/bash

mkdir -p $REGCM/data/REGCM_GLOBEDAT
export REGCM_GLOBEDAT=$REGCM/data/REGCM_GLOBEDAT
export ICTP_DATABASE=http://clima-dods.ictp.it/d8/cordex

cd $REGCM_GLOBEDAT
mkdir SURFACE CLM CLM45 SST EIN15
     
#Dados de superfície:
cd SURFACE
  #Topografia
  curl -o GTOPO_DEM_30s.nc ${ICTP_DATABASE}/SURFACE/GTOPO_DEM_30s.nc

  #Classificação do solo
  curl -o GLCC_BATS_30s.nc ${ICTP_DATABASE}/SURFACE/GLCC_BATS_30s.nc

  #Profundidade lagos
  curl -o ETOPO_BTM_30s.nc ${ICTP_DATABASE}/SURFACE/ETOPO_BTM_30s.nc

  #Textura
  curl -o GLZB_SOIL_30s.nc ${ICTP_DATABASE}/SURFACE/GLZB_SOIL_30s.nc


#SST: temperarua de superfície do mar
#Instruções: ftp://ftp.cdc.noaa.gov/pub/Datasets/noaa.oisst.v2/README
  cd ../SST
  wget ftp://ftp.cdc.noaa.gov/pub/Datasets/noaa.oisst.v2/sst.wkmean.1981-1989.nc
  wget ftp://ftp.cdc.noaa.gov/pub/Datasets/noaa.oisst.v2/sst.wkmean.1990-present.nc

#Dados EIN15
cd ../EIN15
  mkdir 1990
  cd 1990
  #roda loop shell (baixara 20 arquivos):
  for type in air hgt rhum uwnd vwnd
  do
    for hh in 00 06 12 18
    do
      curl -o ${type}.1990.${hh}.nc ${ICTP_DATABASE}/EIN15/1990/${type}.1990.${hh}.nc
    done
  done

Criar diretórios para rodar modelo:

    cd $REGCM
    mkdir REGCM_RUN
    cd REGCM_RUN
    mkdir input output
 
Configurar namelist.in a partir de um modelo:

    cp $REGCM/RegCM-4.4.1/Testing/test_001.in $REGCM/REGCM_RUN/rodada_teste.in

Alterar, dentre outros paramêtros:

     dirter = 'input'
     inpter = '/caminho-para-REGCM_GLOBEDAT'
     dirglob = 'input'
     inpglob = '/caminho-para-REGCM_GLOBEDAT'
     dirout = 'output'
     domname = 'rodada_teste'

Pré-processamento do modelo:

     terrain maria.in 
     sst maria.in
     icbc maria
        
Rodar simulação:

    mpirun -np 8 regcmMPI maria.in

Abrir arquivos gerados na pasta input/output usando GrADSNcPlot: 

- input/exemplo_001_DOMAIN000.nc contém dados de topografia, uso da terra, projeção informação e land sea mask.
- input/exemplo_001_SST.nc fornece ?
- input/exemplo_001_ICBC*.nc fornecem as condições iniciais e de contorno: pressão da superficie, temperatura da superficie, componentes do vento horizontal em 3D, temperatura em 3D, taxa de mistura do DOMAIN para o período e resolução temporal especificada. 
- output/exemplo_001_ATM*.nc: atmosfera status 
- output/exemplo_001_RAD*.nc: variáveis de superficie
- output/exemplo_001_SRF*.nc: fluxo de radiação
- output/exemplo_001_SAV*.nc: status do modelo no final da simulação (permite quebrar a simulação em várias partes)

Rodar esse comandos do grads no pronpt aberto:

./GrADSNcPlot input/exemplo_DOMAIN000.nc

query file
set gxout shaded
set mpdset hires
set cint 50
display topo
clear
set cint 1
display landuse