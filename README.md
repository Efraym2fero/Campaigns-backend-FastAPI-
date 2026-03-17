# Campaign Management API

A simple REST API built with FastAPI and SQLModel to manage marketing campaigns.
The API supports creating, reading, updating, and deleting campaigns and uses SQLite as the database.

---

## 🚀 Features

* RESTful API built with FastAPI
* SQLite database integration
* Automatic database table creation
* Dependency-injected database sessions
* CRUD operations for campaigns
* Generic API response model
* Automatic API documentation

---

## 🛠 Tech Stack

* Python
* FastAPI
* SQLModel
* SQLite
* Uvicorn
* Pydantic

---

## 📁 Project Structure

```
project/
│
├── main.py
├── data.db
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Efraym2fero/Campaigns-backend-FastAPI-.git
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

Windows

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn sqlmodel
```

or

```bash
pip install -r requirements.txt
```

---

##  Running the Server

Start the API server with:

```bash
uvicorn main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically generates API docs.

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## 📌 API Endpoints

### Root

```
GET /
```

Response:

```json
{
  "message": "You are in the root"
}
```

---

### Get All Campaigns

```
GET /campaigns
```

---

### Get Campaign by ID

```
GET /campaigns/{id}
```

---

### Create Campaign

```
POST /campaigns
```

Request body:

```json
{
  "campName": "New Campaign",
  "campDate": "2026-01-01T10:00:00"
}
```

---

### Update Campaign

```
PUT /campaigns/{id}
```

---

### Delete Campaign

```
DELETE /campaigns/{id}
```

---

## 🗄 Database

The application uses SQLite.

Database file:

```
data.db
```

Tables are automatically created on application startup.

---

## Example Campaign Model

```python
class Campaign(SQLModel, table=True):
    campID: int | None = Field(default=None, primary_key=True)
    campName: str
    campDate: datetime | None = None
    createdAt: datetime
```

---

## Example Response

```json
{
  "data": {
    "campID": 1,
    "campName": "hello world",
    "campDate": "2026-03-15T10:00:00",
    "createdAt": "2026-03-15T10:00:00"
  }
}
```
## Pagination Support

### 1) Page-Based 

The API supports pagination for retrieving campaigns efficiently.

### Endpoint

```http
GET /campaigns?page=1&pageSize=10
```

### Query Parameters

| Parameter  | Type | Default | Description                            |
| ---------- | ---- | ------- | -------------------------------------- |
| `page`     | int  | 1       | Page number (must be ≥ 1)              |
| `pageSize` | int  | 10      | Number of items per page (must be ≥ 1) |

---

### Example Request

```http
GET /campaigns?page=2&pageSize=5
```

---

### Example Response

```json
{
  "data": [
    {
      "campID": 6,
      "campName": "campaign 6",
      "campDate": "2026-03-17T10:00:00",
      "createdAt": "2026-03-17T10:00:00"
    }
  ],
  "next": "http://127.0.0.1:8000/campaigns?page=3&pageSize=5",
  "prev": "http://127.0.0.1:8000/campaigns?page=1&pageSize=5"
}
```

---

### 🔍 How It Works

* Uses `limit` and `offset` for efficient database queries
* Returns:

  * `data` → current page results
  * `next` → URL for next page (if exists)
  * `prev` → URL for previous page (if exists)
* Automatically calculates total records using:

```python
select(func.count()).select_from(Campaign)
```

---

### ⚡ Notes

* If there is no next page → `next = null`
* If you are on the first page → `prev = null`
---

### 2) Offset-Based

The API supports **offset-based pagination**, which is efficient and flexible for large datasets.

---

### Endpoint

```http
GET /campaigns?offset=0&limit=10
```

---

### Query Parameters

| Parameter | Type | Default | Description                               |
| --------- | ---- | ------- | ----------------------------------------- |
| `offset`  | int  | 0       | Number of records to skip (must be ≥ 0)   |
| `limit`   | int  | 10      | Number of records to return (must be ≥ 1) |

---

### Example Request

```http
GET /campaigns?offset=10&limit=5
```

---

### Example Response

```json
{
  "data": [
    {
      "campID": 11,
      "campName": "campaign 11",
      "campDate": "2026-03-17T10:00:00",
      "createdAt": "2026-03-17T10:00:00"
    }
  ],
  "next": "http://127.0.0.1:8000/campaigns?offset=15&limit=5",
  "prev": "http://127.0.0.1:8000/campaigns?offset=5&limit=5"
}
```

---

### 🔍 How It Works

* `offset` → how many records to skip
* `limit` → how many records to return
* Data is fetched using:

```python
select(Campaign).offset(offset).limit(limit)
```

---

### 🔗 Navigation URLs

* `next` → points to the next set of results
* `prev` → points to the previous set

Logic:

* If `offset + limit < total` → next page exists
* If `offset > 0` → previous page exists

---

### ⚡ Notes

* If no more data → `next = null`
* If at the beginning → `prev = null`
* Works well with infinite scroll and APIs

---

---

###  Offset vs Page-Based Pagination

| Type   | Pros             | Cons                    |
| ------ | ---------------- | ----------------------- |
| Offset | Simple, flexible | Slower on huge datasets |
| Page   | Easy for users   | Less flexible           |
| Cursor | Best performance | More complex            |

---

