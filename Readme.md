online_bookstore/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── auth.py
│   ├── dependencies.py
│   ├── exceptions.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── conftest.py
├── requirements.txt
└── README.md

# Online Bookstore API

A complete REST API for managing a bookstore built with FastAPI.

## Features

- User authentication (JWT tokens)
- Book and author management
- Shopping cart functionality
- Order processing
- Email notifications (background tasks)
- Advanced filtering and search
- Role-based access control

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## to run
uvicorn app.main:app --reload   