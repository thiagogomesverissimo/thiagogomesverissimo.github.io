Dependências:

    sudo apt-get install pdftk ghostscript xpdf-utils

Separar páginas do pdf

    pdftk largepdfile.pdf burst

Juntar vários arquivos pdf em um único:

    pdftk 1.pdf 2.pdf 3.pdf cat output 123.pdf

Verificar metadados do pdf:

    pdftk arquivo.pdf dump_data

    qpdf -show-encryption arquivo.pdf

Remover metadados convertendo e desconvertendo em ps:

    pdftops [your_protected_pdf_document.pdf] out.ps
    ps2pdf [out.ps] broken_protection_pdf_document.pdf 

qpdf --decrypt input.pdf output.pdf
