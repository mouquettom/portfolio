#!/usr/bin/env sh

set -eu

rm -rf public
mkdir -p public

cp index.html public/
cp style.css public/
cp script.js public/
cp robots.txt sitemap.xml public/

# Version française
cp -R fr public/

cp -R ressources public/

echo "Static site prepared in ./public"