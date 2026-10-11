#!/usr/bin/env sh

set -eu

rm -rf public
mkdir -p public

# Version anglaise
cp index.html public/

# Fichiers partagés
cp style.css public/
cp script.js public/

# SEO anglais
cp robots.txt public/robots.txt
cp sitemap.xml public/sitemap.xml

# Ressources
cp -R ressources public/

echo "English static site prepared in ./public"
