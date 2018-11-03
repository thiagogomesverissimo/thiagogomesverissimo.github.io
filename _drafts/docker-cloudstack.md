#!/bin/bash

export CLOUDSTACK_API_URL='https://internuvem.usp.br/client/api'
export CLOUDSTACK_API_KEY=''
export CLOUDSTACK_SECRET_KEY=''
  
#  --cloudstack-use-port-forward ?? \
# --cloudstack-use-private-address	

docker-machine create -d cloudstack \
  --cloudstack-template "Ubuntu 16.04 - Oficial" \
  --cloudstack-zone "IDC3-NUVEM (NUVEM)" \
  --cloudstack-service-offering "Mini (1vCPU, 512MB RAM)" \
  --cloudstack-network "nuvem-FFLCH" \
  --cloudstack-public-ip "200.144.254.73" \
  --cloudstack-ssh-user "ubuntu" \
  --cloudstack-expunge \
  docker-machine-9
