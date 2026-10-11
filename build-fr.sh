#!/usr/bin/env bash

set -eu

rm -rf public-fr
mkdir -p public-fr

# Version française comme page racine
cp fr/index.html public-fr/index.html

# Fichiers partagés
cp style.css public-fr/
cp script.js public-fr/

# SEO français
cp robots-fr.txt public-fr/robots.txt
cp sitemap-fr.xml public-fr/sitemap.xml

# Ressources
cp -R ressources public-fr/

echo "French static site prepared in ./public-fr"
