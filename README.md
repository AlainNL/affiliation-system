# API d'Affiliation

This API allows an affiliate partner to manage relationships between advertisers and publishers, as well as track orders generated through affiliate links.

## Table of contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Endpoints API](#endpoints-api)
  - [Advisers](#advisers)
  - [Applications](#applications)
  - [Orders](#orders)
- [Data Models](#data-models)
- [Tests](#tests)
- [Passage à l'échelle](#passage-à-léchelle)

## Installation

### Prerequiites

- Python 3.9+
- pip
- Docker et Docker Compose (optionnel)

### Local Installation

1. Clone the repository
```bash
git clone https://github.com/AlainNL/affiliation-system.git
cd affiliation-api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configurer environment variables
```bash
cp .env.
```

### Installation with Docker

1. Cloner le dépôt
```bash
git clone https://github.com/AlainNL/affiliation-system.git
cd affiliation-api
```

2. Build and start the containers
```bash
docker-compose up -d
```

## Quick Start

### Run loccaly

```bash
python run.py
```

The API will be available at `http://localhost:5000`.

### Run Tests

```bash
pytest
```

## Endpoints API

The API is organized around three main resources:

### Advertisers

#### Retrieves all advertisers

```
GET /api_membership/advertisers
```

Retrieves the list of advertisers available to a publisher.

#### Récupérer un annonceur

```
GET /api_membership/advertisers/<advertiser_id>
```

Retrieves details of a specific advertiser.


### Applications

#### Create an application

```
POST /api/v1/applications
```

Crée une candidature pour un annonceur.

Corps de la requête:
```json
{
  "publisher_id": "publisher_1",
  "advertiser_id": "user_2"
}
```

#### Récupérer les candidatures d'un éditeur

```
GET /api/v1/applications?publisher_id={publisher_id}
```

Récupère la liste des candidatures d'un éditeur.

#### Récupérer une candidature

```
GET /api/v1/applications/{application_id}
```

Récupère les détails d'une candidature spécifique.


### Commandes

#### Récupérer les commandes d'un éditeur

```
GET /api/v1/orders?publisher_id={publisher_id}
```

Récupère la liste des commandes d'un éditeur. Des paramètres de filtrage peuvent être ajoutés:
- `advertiser_id`: Filtrer par annonceur
- `from_date`: Date de début (format ISO 8601)
- `to_date`: Date de fin (format ISO 8601)

#### Récupérer une commande

```
GET /api/v1/orders/{order_id}
```

Récupère les détails d'une commande spécifique.

#### Simuler une commande (pour les tests)

```
POST /api/v1/orders/track
```

Simule le tracking d'une commande (fonctionnalité de test).

Corps de la requête:
```json
{
  "advertiser_id": "user_1",
  "publisher_id": "publisher_1",
  "user_id": "1",
  "amount": 129.99,
  "tracking_params": {"campaign": "summer_sale"}
}

```

## Modèles de données

### Annonceur (Advertiser)

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "website": "string",
  "commission_rate": "number",
  "category": "string",
  "is_active": "boolean"
}
```

### Candidature (Application)

```json
{
  "id": "string",
  "advertiser_id": "string",
  "publisher_id": "string",
  "status": "string (pending, approved, rejected)",
  "application_date": "string (ISO 8601)",
