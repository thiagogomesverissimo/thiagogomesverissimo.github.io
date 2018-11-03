latex updated version 

wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
tar -vzxf install-tl-unx.tar.gz 
cd install-tl-20161010/ # ou o nome da pasta descompactada
sudo ./install-tl
sudo ln -s /usr/local/texlive/2016/bin/x86_64-linux/* /usr/local/bin/


sudo add-apt-repository ppa:jonathonf/texlive
sudo apt-get update


# Convertendo para doc usando tex4ht:
    
    apt-get install tex4ht
    latex filename.tex
    bibtex filename.aux
    mk4ht oolatex filename.tex

# Convertendo para doc usando pandoc:

    pandoc -f latex -t odt -o output.odt input.tex
