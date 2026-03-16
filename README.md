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

## ▶️ Running the Server

Start the API server with:

```bash
uvicorn main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## 📚 API Documentation

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

## 📦 Example Campaign Model

```python
class Campaign(SQLModel, table=True):
    campID: int | None = Field(default=None, primary_key=True)
    campName: str
    campDate: datetime | None = None
    createdAt: datetime
```

---

## 🧪 Example Response

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
