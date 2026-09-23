#!/usr/bin/env sh

set -eu

rm -rf public
mkdir -p public

cp index.html public/
cp style.css public/
cp script.js public/

cp -R ressources public/

echo "Static site prepared in ./public"