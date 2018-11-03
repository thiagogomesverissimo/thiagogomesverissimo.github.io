Pacote
 apt-get install lvm2

Transformar os discos físicos em PV (Physical Volume): 
  pvcreate /dev/xvdb /dev/xvdc /dev/xvde
  pvdisplay -C

Criar um grupo com todos PVs acima: 
  vgcreate vg_meugrupo /dev/xvdb /dev/xvdc /dev/xvde
  vgdisplay

Criar o LV ("partição virtual" - logical volume): 
  lvcreate -n lv_meulv -l 100%FREE  vg_meugrupo
  lvdisplay -C

Formatar: 
  mkfs.ext4 /dev/vg_meugrupo/lv_meulv

Montar LV: 
  mount /dev/mapper/vg_meugrupo-lv_meulv /pasta_desejada

No /etc/fstab: 
  /dev/mapper/vg_meugrupo-lv_meulv /pasta_desejada ext4    defaults   0      2

Para aumentar o LV adcionando outros discos físicos:
  pvcreate /dev/sda1
  vgextend vg_meugrupo /dev/sda1
  lvextend -n /dev/mapper/vg_meugrupo-lv_meulv -l 100%FREE
  ou lvextend -L+222M /dev/mapper/vg_meugrupo-lv_meulv
  ou lvextend -L+222G /dev/mapper/vg_meugrupo-lv_meulv
  resize2fs /dev/mapper/vg_meugrupo-lv_meulv


Apagar LV: 
  lvremove /dev/mapper/vg_meugrupo-lv_meulv

Conferir próximo comando
  vgchange -a y


