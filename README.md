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
- [Scalability](#Scalability])

## Installation

### Prerequites

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

## API Endpoints

### 1. Advertisers
#### Retrieve the list of advertisers
- **GET** `/api_membership/advertisers`
- **Description**: Retrieves the list of advertisers available to a publisher.
- **Optional Parameter**:
  - `publisher_id` (query param) - Publisher's identifier.

#### Retrieve advertiser details
- **GET** `/api_membership/advertisers/<advertiser_id>`
📝 *Replace `<advertiser_id>` with the actual advertiser's ID. Example: `user_1`, `user_2`, `user_3`.*
- **Description**: Retrieves details of a specific advertiser.
- **Parameter**:
  - `advertiser_id` (URL param) - Advertiser's identifier.

---

### 2. Applications
#### Apply to an advertiser
- **POST** `/api_membership/applications`
- **Description**: Allows a publisher to apply to an advertiser.
- **Required JSON Body**:
  ```json
  {
    "publisher_id": "publisher_1",
    "advertiser_id": "user_1"
  }

### 3. Orders

#### Retrieve orders
- **Method:** `GET`
- **Endpoint:** `/api_membership/orders?publisher_id=<publisher_id>`
📝 *Replace `<publisher_id>` with the actual publisher's ID. Example: `publisher_1`, `publisher_2`.*
- **Description:** Retrieves a publisher's orders with optional filters.

**Required Parameters:**
| Parameter      | Type   | Description               |
|---------------|--------|---------------------------|
| `publisher_id` | string | Publisher's identifier   |

**Optional Parameters:**
| Parameter    | Type   | Description                |
|-------------|--------|----------------------------|
| `advertiser_id` | string | Filter by advertiser   |
| `from_date` | string (ISO 8601) | Start date |
| `to_date`   | string (ISO 8601) | End date   |

---

#### Track an order
- **Method:** `POST`
- **Endpoint:** `/api_membership/orders/track`
- **Description:** Simulates an order and records the data.

**Request Body (JSON):**
```json
{
  "advertiser_id": "user_2",
  "publisher_id": "publisher_2",
  "user_id": "2",
  "amount": 49.99,
  "tracking_params": {
    "campaign": "flash_sale",
    "source": "mobile_app"
  }
}


```

## Modèles de données

### Advertiser

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "website": "string",
  "commission_rate": "float",
  "category": "string",
  "is_active": "boolean"
}
```

### Application

```json
{
  "id": "string",
  "advertiser_id": "string",
  "publisher_id": "string",
  "status": "string (pending, approved, rejected)",
  "application_date": "string (ISO 8601)",
}
```

### Orders

```json
{
  "id": "string",
  "advertiser_id": "string",
  "publisher_id": "string",
  "user_id": "string",
  "amount": "float",
  "commission": "float",
  "status": "string (pending, approved, rejected)",
  "order_date": "string (ISO 8601)",
  "validation_date": "string (ISO 8601)",
  "tracking_params": {
    "campaign": "string",
    "source": "string (optional)"
  }
}

```

## Tests

### Running Tests

To run the tests, execute the following command:

```bash
pytest
```
We use `pytest` as our testing framework. It supports fixtures, assertions, and various plugins to extend functionality, making it easier to write and manage tests.

### Advertiser Tests

- Test: Get All Advertisers
Ensures that the get_all_advertisers method correctly returns a list of advertisers.
```python
def test_get_all_advertisers(test_advertiser_service):
    advertisers = list(test_advertiser_service.get_all_advertisers("some_publisher_id"))
    assert len(advertisers) == 3
```

- Test: Generate Tracking URL
Ensures that a tracking URL is generated correctly for an advertiser.
```python
def test_get_advertiser_tracking_url(test_advertiser_service):
    tracking_url = test_advertiser_service.get_advertiser_tracking_url(advertiser.id, publisher_id, user_id)
    assert tracking_url is not None
```


### API Endpoints tests

- Test: Get Advertisers
Tests the GET /api_membership/advertisers endpoint, checking the response status and data.
``` python
def test_get_advertisers(client):
   response = client.get('/api_membership/advertisers')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) > 0
    advertiser_id = data['data'][0]['id']
    assert advertiser_id is not None, "Advertiser ID is None"
```

- Test: Get Specific Advertiser
Tests the GET /api_membership/advertisers/<advertiser_id> endpoint to retrieve a specific advertiser.
```python
def test_get_advertiser(client):
    response = client.get(f'/api_membership/advertisers/{advertiser_id}')
    assert response.status_code == 200
```

- Test: Apply to Advertiser via API
Tests the POST /api_membership/applications endpoint to apply to an advertiser.
```python
def test_apply_to_advertiser(client):
    response = client.get('/api_membership/advertisers')
    data = json.loads(response.data)
    advertiser_id = data['data'][0]['id']


    publisher_id = "test_publisher"
    response = client.post('/api_membership/applications',
                        json={"publisher_id": publisher_id, "advertiser_id": advertiser_id})


    data = json.loads(response.data)
    assert response.status_code == 201
    assert data['success'] is True
    assert "application_id" in data['data']
    assert data['data']["advertiser_id"] == advertiser_id
```

- Test: Get Orders
Tests the GET /api_membership/orders endpoint to retrieve the list of orders for a publisher.
```python
def test_get_orders(client):
    response = client.get('/api_membership/orders?publisher_id=test_publisher')
    assert response.status_code == 200
````

## Tests
