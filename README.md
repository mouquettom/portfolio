# Orange County Lettings

[![CI](https://github.com/mouquettom/orange-county-lettings/actions/workflows/ci.yml/badge.svg)](https://github.com/mouquettom/orange-county-lettings/actions/workflows/ci.yml)

Application web Django de gestion de locations immobilières et de profils utilisateurs, refactorisée et industrialisée dans le cadre de la formation **Développeur d'application Python** d'OpenClassrooms.

Le projet met notamment en œuvre :

- une architecture Django modulaire ;
- des tests automatisés avec Pytest ;
- une couverture de tests supérieure à 80 % ;
- du linting avec Flake8 ;
- la journalisation Python et la remontée d'erreurs avec Sentry ;
- une conteneurisation Docker ;
- un pipeline CI/CD avec GitHub Actions ;
- une publication automatique de l'image sur Docker Hub ;
- un déploiement automatique sur Render.

---

## Sommaire

- [Aperçu](#aperçu)
- [Application en production](#application-en-production)
- [Technologies](#technologies)
- [Architecture du projet](#architecture-du-projet)
- [Base de données](#base-de-données)
- [Installation locale](#installation-locale)
- [Variables d'environnement](#variables-denvironnement)
- [Lancer l'application](#lancer-lapplication)
- [Tests et qualité](#tests-et-qualité)
- [Logging et Sentry](#logging-et-sentry)
- [Docker](#docker)
- [CI/CD](#cicd)
- [Déploiement](#déploiement)
- [Commandes utiles](#commandes-utiles)

---

## Aperçu

Orange County Lettings permet de consulter :

- la liste des locations ;
- le détail d'une location et de son adresse ;
- la liste des profils utilisateurs ;
- le détail d'un profil ;
- l'interface d'administration Django.

L'application a été refactorisée afin de séparer les responsabilités en plusieurs applications Django :

- `oc_lettings_site` : configuration générale du projet et pages globales ;
- `lettings` : gestion des locations et des adresses ;
- `profiles` : gestion des profils utilisateurs.

Des pages personnalisées sont également disponibles pour les erreurs HTTP `404` et `500`.

---

## Application en production

Application publique :

**https://orange-county-lettings-a4ee.onrender.com/**

Image Docker publique :

**`tommouquet/orange-county-lettings`**

La version la plus récente peut être récupérée avec :

```bash
docker pull tommouquet/orange-county-lettings:latest
```

Chaque build réalisé depuis `master` est également publié avec un tag correspondant au SHA du commit Git.

---

## Technologies

### Back-end

- Python 3.9
- Django 3.0
- SQLite3
- Gunicorn

### Qualité et tests

- Pytest
- pytest-django
- pytest-cov
- Coverage
- Flake8

### Production et observabilité

- Sentry
- Python logging
- WhiteNoise
- python-dotenv

### DevOps

- Docker
- Docker Hub
- GitHub Actions
- Render

---

## Architecture du projet

Structure simplifiée :

```text
orange-county-lettings/
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── lettings/
│   ├── migrations/
│   ├── templates/
│   │   └── lettings/
│   ├── tests/
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── profiles/
│   ├── migrations/
│   ├── templates/
│   │   └── profiles/
│   ├── tests/
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── oc_lettings_site/
│   ├── tests/
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
│
├── static/
├── templates/
├── Dockerfile
├── manage.py
├── requirements.txt
├── setup.cfg
├── .env.example
└── oc-lettings-site.sqlite3
```

### Applications Django

#### `lettings`

Cette application contient les modèles :

- `Address`
- `Letting`

Elle gère :

- la liste des locations ;
- le détail d'une location ;
- les adresses associées aux locations.

#### `profiles`

Cette application contient le modèle :

- `Profile`

Elle gère :

- la liste des profils ;
- le détail d'un profil utilisateur.

#### `oc_lettings_site`

Cette application contient notamment :

- la page d'accueil ;
- la configuration générale Django ;
- les handlers d'erreurs `404` et `500` ;
- les URLs racines du projet.

---

## Base de données

Le projet utilise **SQLite3**.

### Modèles principaux

#### Address

Une adresse contient notamment :

- un numéro ;
- une rue ;
- une ville ;
- un État ;
- un code postal ;
- un code pays ISO.

#### Letting

Une location possède :

- un titre ;
- une relation `OneToOne` vers une `Address`.

#### Profile

Un profil possède :

- une relation `OneToOne` vers le modèle Django `User` ;
- une ville favorite facultative.

Schéma simplifié :

```text
User
  │
  └── 1 — 1 ── Profile

Letting
  │
  └── 1 — 1 ── Address
```

---

## Installation locale

### 1. Cloner le repository

```bash
git clone https://github.com/mouquettom/orange-county-lettings.git
cd orange-county-lettings
```

### 2. Créer un environnement virtuel

macOS / Linux :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows :

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

Créer un fichier `.env` à la racine du projet.

Exemple de configuration locale :

```env
SECRET_KEY=change-me-for-local-development
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

SENTRY_DSN=
SENTRY_ENVIRONMENT=development
```

Le fichier `.env` ne doit jamais être versionné.

### 5. Appliquer les migrations

```bash
python manage.py migrate
```

---

## Variables d'environnement

Les principales variables utilisées par l'application sont :

| Variable | Description | Exemple local |
| --- | --- | --- |
| `SECRET_KEY` | Clé secrète Django | `change-me-for-local-development` |
| `DEBUG` | Active ou désactive le mode debug | `True` |
| `ALLOWED_HOSTS` | Hôtes autorisés, séparés par des virgules | `127.0.0.1,localhost` |
| `SENTRY_DSN` | DSN du projet Sentry | vide si Sentry n'est pas utilisé |
| `SENTRY_ENVIRONMENT` | Nom de l'environnement Sentry | `development` |

En production, les valeurs sensibles sont configurées directement dans Render et ne sont jamais stockées dans Git.

---

## Lancer l'application

### Serveur de développement Django

```bash
python manage.py runserver
```

L'application est ensuite disponible sur :

```text
http://127.0.0.1:8000/
```

### Interface d'administration

```text
http://127.0.0.1:8000/admin/
```

---

## Tests et qualité

Le projet utilise **Pytest** pour les tests automatisés et **Flake8** pour le contrôle de qualité du code.

Les tests sont organisés dans les applications auxquelles ils appartiennent :

```text
lettings/tests/
profiles/tests/
oc_lettings_site/tests/
```

Ils couvrent notamment :

- les modèles ;
- les URLs ;
- les vues ;
- les templates ;
- les réponses `404` ;
- les handlers `404` et `500` ;
- les logs applicatifs.

### Lancer Flake8

```bash
flake8 oc_lettings_site lettings profiles manage.py
```

Aucune sortie signifie qu'aucune erreur Flake8 n'a été détectée.

### Préparer les fichiers statiques

```bash
python manage.py collectstatic --noinput
```

### Lancer les tests

```bash
pytest
```

### Lancer les tests avec couverture

```bash
pytest --cov=. --cov-report=term-missing --cov-fail-under=80
```

Le pipeline CI impose une couverture minimale de **80 %**.

Lors de la validation du projet, la suite comportait **18 tests** avec une couverture d'environ **96 %**.

---

## Logging et Sentry

L'application utilise le module standard `logging` de Python.

Des logs sont notamment générés dans :

- `lettings` ;
- `profiles` ;
- `oc_lettings_site`.

Exemples de niveaux utilisés :

- `INFO` pour les actions normales ;
- `WARNING` lorsqu'une ressource demandée n'existe pas ;
- `ERROR` pour les erreurs remontées à Sentry.

### Sentry

Sentry centralise les exceptions et facilite le suivi des erreurs en production.

La configuration repose sur les variables :

```env
SENTRY_DSN=
SENTRY_ENVIRONMENT=development
```

En production :

```text
SENTRY_ENVIRONMENT=production
```

Le DSN Sentry n'est jamais stocké directement dans le code source.

---

## Docker

Le projet est entièrement conteneurisé.

Le `Dockerfile` :

1. utilise une image Python 3.9 légère ;
2. installe les dépendances ;
3. copie le code du projet ;
4. exécute `collectstatic` ;
5. expose le port `8000` pour l'utilisation locale ;
6. démarre l'application avec Gunicorn.

Gunicorn écoute :

```text
${PORT:-8000}
```

Cela permet d'utiliser :

- le port `8000` par défaut en local ;
- le port fourni automatiquement par Render en production.

### Construire l'image localement

```bash
docker build -t orange-county-lettings:local .
```

### Lancer l'image locale

```bash
docker run --rm \
  -p 8000:8000 \
  --env-file .env \
  orange-county-lettings:local
```

Puis ouvrir :

```text
http://127.0.0.1:8000/
```

### Récupérer l'image depuis Docker Hub

```bash
docker pull tommouquet/orange-county-lettings:latest
```

### Lancer l'image Docker Hub

```bash
docker run --rm \
  -p 8000:8000 \
  --env-file .env \
  tommouquet/orange-county-lettings:latest
```

---

## CI/CD

Le workflow est défini dans :

```text
.github/workflows/ci.yml
```

### Push sur une branche

À chaque push, GitHub Actions exécute le job de qualité :

```text
Checkout
   ↓
Python 3.9
   ↓
Installation des dépendances
   ↓
Flake8
   ↓
collectstatic
   ↓
Pytest + Coverage >= 80 %
```

Les Pull Requests vers `master` exécutent également ces vérifications.

### Push sur `master`

Lors d'un push sur `master`, si le job de tests réussit, le pipeline continue :

```text
Tests and code quality
          ↓
Build and push Docker image
          ↓
Deploy to Render
```

Une version invalide ne peut donc pas être publiée ni déployée si les tests, Flake8 ou la couverture échouent.

### Publication Docker

Le pipeline publie la même image Docker avec deux tags :

```text
tommouquet/orange-county-lettings:latest
tommouquet/orange-county-lettings:<SHA_DU_COMMIT>
```

`latest` pointe vers la version la plus récente.

Le tag SHA permet d'identifier précisément l'image correspondant à un commit Git donné.

### Secrets GitHub Actions

Dans :

```text
Repository
→ Settings
→ Secrets and variables
→ Actions
```

Configurer :

#### Repository variable

```text
DOCKERHUB_USERNAME
```

#### Repository secrets

```text
DOCKERHUB_TOKEN
RENDER_DEPLOY_HOOK_URL
```

Ces valeurs ne doivent jamais être écrites directement dans `ci.yml`.

---

## Déploiement

L'application est déployée sur **Render** à partir de l'image publiée sur **Docker Hub**.

Architecture :

```text
Code local
    ↓
Git push
    ↓
GitHub
    ↓
GitHub Actions
    ↓
Flake8 + Pytest + Coverage
    ↓
Docker build
    ↓
Docker Hub
    ↓
Render Deploy Hook
    ↓
Render
    ↓
Docker container
    ↓
Gunicorn
    ↓
Django
    ↓
HTTPS public
```

### Configuration Render

Le service utilise l'image :

```text
docker.io/tommouquet/orange-county-lettings:latest
```

Variables d'environnement de production à configurer :

```text
SECRET_KEY=<clé de production>
DEBUG=False
ALLOWED_HOSTS=orange-county-lettings-a4ee.onrender.com
SENTRY_DSN=<DSN Sentry>
SENTRY_ENVIRONMENT=production
```

Ne pas ajouter :

- `https://` dans `ALLOWED_HOSTS` ;
- de slash final dans `ALLOWED_HOSTS` ;
- de secret directement dans le repository.

### Fichiers statiques

Les fichiers statiques sont préparés avec :

```bash
python manage.py collectstatic --noinput
```

Ils sont servis en production avec **WhiteNoise**.

### Serveur de production

Django n'est pas lancé avec `runserver` en production.

Le conteneur démarre **Gunicorn** avec deux workers et utilise le port fourni par Render :

```text
0.0.0.0:${PORT:-8000}
```

### Déploiement automatique

Après un push sur `master` :

1. GitHub Actions lance les tests ;
2. si les tests réussissent, l'image Docker est construite ;
3. l'image est publiée sur Docker Hub ;
4. le Deploy Hook Render est appelé ;
5. Render récupère la nouvelle image ;
6. le service redémarre avec la nouvelle version.

Une simple modification du code suivie d'un commit et d'un push sur `master` est donc déployée automatiquement si la CI est verte.

---

## Commandes utiles

### Développement

```bash
python manage.py runserver
```

### Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Tests

```bash
pytest
```

### Coverage

```bash
pytest --cov=. --cov-report=term-missing --cov-fail-under=80
```

### Flake8

```bash
flake8 oc_lettings_site lettings profiles manage.py
```

### Fichiers statiques

```bash
python manage.py collectstatic --noinput
```

### Docker build

```bash
docker build -t orange-county-lettings:local .
```

### Docker run

```bash
docker run --rm -p 8000:8000 --env-file .env orange-county-lettings:local
```

### Docker Hub pull

```bash
docker pull tommouquet/orange-county-lettings:latest
```

---

## Sécurité

- Les secrets ne sont jamais stockés dans le repository.
- `.env` est utilisé uniquement pour la configuration locale.
- Les secrets de CI/CD sont stockés dans GitHub Actions.
- Les variables de production sont stockées dans Render.
- `DEBUG` est désactivé en production.
- Sentry est configuré via variables d'environnement.
- Le déploiement Docker/Render ne se produit qu'après réussite des contrôles automatisés.

---

## Projet OpenClassrooms

Ce projet a été réalisé dans le cadre du parcours **Développeur d'application Python** d'OpenClassrooms.

Les principaux objectifs techniques étaient :

- refactoriser une application Django monolithique ;
- améliorer la qualité du code ;
- ajouter des tests automatisés ;
- mettre en place la journalisation et Sentry ;
- créer un pipeline CI/CD ;
- conteneuriser l'application avec Docker ;
- publier l'image sur Docker Hub ;
- déployer l'application en production ;
- préparer une documentation technique complète.