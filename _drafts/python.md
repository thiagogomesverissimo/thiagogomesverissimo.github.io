Instalação do pip e virtualenv:

    sudo apt-get install python-setuptools
    sudo easy_install pip
    sudo pip install virtualenv

Criando, acessando e instalando bibliotecas virtualenv thiagolibs:

    virtualenv -p python3 ~/.mypythonlibs
    . ~/.mypythonlibs/bin/activate
    ~/.mypythonlibs/bin/pip3 install flask
    deactivate

Listar bibliotecas instaladas em thiagolibs:

    ~/.mypythonlibs/bin/pip3 freeze > requirements.txt

Instalar bibliotecas a partir de uma arquivo:

    ~/.mypythonlibs/bin/pip3 install -r requirements.txt
