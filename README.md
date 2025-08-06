# Inventory Management API

A simple and robust asynchronous API for managing a product inventory. Built with **FastAPI**, **SQLAlchemy**, and **Alembic**, this project provides full CRUD (Create, Read, Update, Delete) functionality for products and allows for tracking stock movements.

---

##  Stack

-   **Framework:** FastAPI
-   **ORM:** SQLAlchemy (with async support)
-   **Database:** SQLite
-   **Migrations:** Alembic
-   **Data Validation:** Pydantic
-   **Server:** Uvicorn

---

##  Folder Structure

```

inventory-api/
│
├── alembic/              \# Holds database migration scripts
│   └── versions/
├── app/                  \# Main application source code
│   ├── api/              \# API endpoint definitions
│   │   └── endpoints.py
│   ├── **init**.py
│   ├── crud.py           \# Database operation functions
│   ├── database.py       \# DB engine and session setup
│   ├── main.py           \# FastAPI app entry point
│   ├── models.py         \# SQLAlchemy table models
│   └── schemas.py        \# Pydantic data models
│
├── venv/                 \# Virtual environment
├── alembic.ini           \# Alembic configuration file
├── inventory.db          \# SQLite database file (created after migration)
└── requirements.txt      \# Project dependencies

````

---

##  Local Setup Instructions

### 1\. Clone the Repository

```bash
git clone https://github.com/mevamsireddy/simple-inventory-management.git
cd inventory-api
````

### 2\. Create and Activate Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the environment
# On Windows:
.\venv\Scripts\activate
```

### 3\. Install Dependencies

Install all the required packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4\. Initialize the Database

Run the Alembic migration command to create the necessary tables in the SQLite database. This command reads from your `app/models.py` file and builds the database schema.

```bash
alembic upgrade head
```

After this command runs, an `inventory.db` file will appear in your project directory.

### 5\. Run the Server

Start the application using the Uvicorn ASGI server.

```bash
uvicorn app.main:app --reload
```

The API will now be running at `http://127.0.0.1:8000`. The `--reload` flag makes the server restart automatically after code changes.

### 6\. Access Interactive API Docs

FastAPI provides automatic interactive documentation. Once the server is running, navigate to one of the following URLs in your browser:

  - **Swagger UI:** `http://127.0.0.1:8000/docs`
  - **ReDoc:** `http://127.0.0.1:8000/redoc`

-----

##  API Endpoints

| Method  | Path                                 | Description                                  |
| :-----  | :----------------------------------- | :------------------------------------------- |
| `POST`  | `/products/`                         | Add a new product.                           |
| `GET`   | `/products/`                         | List all products.                           |
| `GET`   | `/products/{id}`                     | Get details for a specific product.          |
| `PUT`   | `/products/{id}`                     | Update a product's details.                  |
| `DELETE`| `/products/{id}`                     | Delete a product.                            |
| `POST`  | `/stock/`                            | Record a stock transaction (IN or OUT).      |
| `GET`   | `/stock/`                            | List all stock transactions.                 |
| `GET`   | `/stock/product/{product_id}`        | Get all transactions for a specific product. |

-----

##  Sample API Requests (`curl`)

Here are a few examples of how to interact with the API using `curl` from your terminal.

### 1\. Create a New Product

```bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/products/](http://127.0.0.1:8000/products/)' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Wireless Mouse",
  "description": "A reliable ergonomic wireless mouse.",
  "price": 25.50,
  "available_quantity": 50
}'
```

**Expected Response (201 Created):**

```json
{
  "name": "Wireless Mouse",
  "description": "A reliable ergonomic wireless mouse.",
  "price": 25.5,
  "id": 1,
  "available_quantity": 50
}
```

### 2\. List All Products

```bash
curl -X 'GET' \
  '[http://127.0.0.1:8000/products/](http://127.0.0.1:8000/products/)' \
  -H 'accept: application/json'
```

### 3\. Record a Stock Transaction (Add Stock)

This records an "IN" transaction of 10 units for the product with `id: 1`.

```bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/stock/](http://127.0.0.1:8000/stock/)' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "product_id": 1,
  "quantity": 10,
  "transaction_type": "IN"
}'
```

### 4\. Get Transactions for a Specific Product

This fetches all stock history for the product with `id: 1`.

```bash
curl -X 'GET' \
  '[http://127.0.0.1:8000/stock/product/1](http://127.0.0.1:8000/stock/product/1)' \
  -H 'accept: application/json'
```

```
```
