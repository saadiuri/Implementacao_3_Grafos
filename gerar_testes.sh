#!/bin/bash

for arquivo in Testes/*.txt
do
    echo "Executando $arquivo"
    java Codigos.Main $arquivo
    echo ""
done