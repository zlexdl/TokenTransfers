#!/usr/bin/bash

geth --datadir "/home/ethbase/chain" --rpc --rpcport "8086" --rpccorsdomain "*"  --port "30303" --nodiscover --rpcapi "db,eth,net,web3" --networkid 1006 init /root/genesis.json

