## Sessão

Ver sessões ativas e selecionar: 

    tmux list-sessions (prefix + s)
    
Acessar uma sessão:

    tmux attach -t thiago  (prefix + :new -t thiago)
    
Criar nova sessão:

    tmux new -s thiago_work (prefix + :new -s minha_session)

Renomear sessão: 

    (prefix + $)

Sair de uma sessão:

    tmux detach (or prefix + d)

Matar uma sessão:

    tmux kill-session -t thiago_tmux

## Janelas

Nova Janela (sem nome):
    
    tmux new-window (prefix + c)

Nova Janela (com nome):

    tmux new-window -t minha_sessao:1 -n 'minha_janela' 

Renomear janela:

    (prefix + ,)

Listar e selecionar janela(s): 

    (prefix + w)

Seleciona janela sem listar:

    tmux select-window -t :0-9 (prefix + 0-9)

Dividir janela verticalmente:

    tmux split-window  (ou prefix + %) 

Dividir janela horizoltamente:

    tmux split-window -h (ou prefix + ")

Matar janela:
   
    (prefix + &)
    
## Paniéis

Matar painel
   
    prefix + x
    
## Diversos:

Relógio

    (prefix + t)
    
Listas teclas de atalho:

    (prefix + ?)