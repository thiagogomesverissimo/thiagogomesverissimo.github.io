Criar a partição (se menor que 2TB pode-se fazer com fdisk):

    parted /dev/sdb
    (parted) mklabel gpt
    (parted) unit TB
    (parted) mkpart primary 0.00TB 3.00TB
    (parted) quit

Preparando partição para ser criptografada:

    # dd if=/dev/urandom of=/dev/sdb1
    sudo cryptsetup luksFormat /dev/sdb1
    sudo cryptsetup luksOpen /dev/sdb1 thiagodados
    sudo mkfs.ext4 /dev/mapper/thiagodados
    sudo e2label /dev/mapper/thiagodados thiagodados
    sudo cryptsetup luksClose thiagodados

Abrindo, trabalhando e fechando partição criptografada:

    mkdir ~/thiagodados
    sudo cryptsetup luksOpen /dev/sdb1 thiagodados
    sudo mount /dev/mapper/thiagodados /home/thiago/thiagodados
    sudo chown thiago: /home/thiago/thiagodados/
    sudo umount /home/thiago/thiagodados
    sudo cryptsetup luksClose thiagodados

Criptografar home di usuário thiago depois que o linux já está instalado:
    
    sudo apt-get install ecryptfs-utils rsync 
    sudo modprobe ecryptfs 
    # logado em outro usuário:
    ecryptfs-migrate-home -u thiago 
