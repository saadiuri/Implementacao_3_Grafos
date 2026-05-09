#!/bin/bash

for arquivo in Testes/*.txt
do
    echo "Executando $arquivo"
    java -cp . Codigos.Java.Main $arquivo
    echo ""
done