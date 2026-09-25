# Portfolio

[![Portfolio CI](https://github.com/mouquettom/portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/mouquettom/portfolio/actions/workflows/ci.yml)

Personal portfolio combining my background in motion design with my transition into Python back-end development.

The website presents my profile, technical projects, professional journey and creative background through a minimalist interface enriched with custom Lottie animations.

## Live website

[View the portfolio](https://tom-mouquet-portfolio.onrender.com)

## Tech stack

### Front-end

- HTML5
- CSS3
- JavaScript
- Lottie / Bodymovin

### Testing

- Pytest
- Playwright
- End-to-end browser tests

### DevOps

- Docker
- Nginx
- GitHub Actions
- Render
- Continuous Integration / Continuous Deployment

## Featured projects

### Epic Events

Back-end CRM application built with Python, SQLAlchemy and PostgreSQL.

### SoftDesk API

REST API for collaborative project management using Django REST Framework and JWT authentication.

### LIT-Revu

Django social application based around reviews, tickets and user interactions.

### AlgoInvest & Trade

Python application focused on algorithmic investment optimization.

### Chess Tournament

Offline tournament management application built with Python.

## Continuous Integration

Every push to `main` automatically triggers the CI pipeline:

```text
Push to GitHub
      ↓
Pytest + Playwright
      ↓
Docker image build
      ↓
CI checks passed
      ↓
Render deployment