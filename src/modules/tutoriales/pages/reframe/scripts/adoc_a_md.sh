#!/bin/bash

if [ -z "$1" ]; then
    echo "Uso: $0 archivo-sin-extension"
    exit 1
fi

if [ ! -f "$1.adoc" ]; then
    echo "Error: no existe $1.adoc"
    exit 1
fi

echo "Convirtiendo $1.adoc a $1.xml (archivo docbook)"

asciidoctor -b docbook -o "$1.xml" "$1.adoc"

echo "Convirtiendo $1.xml como docbook a $1.md"

pandoc \
    -f docbook \
    -t markdown \
    --wrap=preserve \
    "$1.xml" \
    -o "$1.md"

if [ $? -ne 0 ]; then
    echo "Error al convertir con pandoc"
    exit 1
fi

echo "reemplazando algunos caracteres en $1.md"

sed -i "s/ {#.*}//g" "$1.md"
sed -i "s/\~\\\~\~/\~\~\~/g" "$1.md"
sed -i "s/\](view-source:/\](/g" "$1.md"

echo "Eliminando archivo docbook"

rm "$1.xml"

echo "Listo"