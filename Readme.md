# 📚 Online Bookstore API

A complete and production-ready **RESTful API** for managing an online bookstore built with **FastAPI**.
This application provides support for authentication, book and author management, ordering workflows, and role-based access for users and administrators.

---

## 🚀 Key Features

| Feature             | Description                                           |
| ------------------- | ----------------------------------------------------- |
| 🔐 Authentication   | Secure user login & registration using **JWT tokens** |
| 👤 User Roles       | Role-based access control — **Admin / Customer**      |
| 📘 Books & Authors  | Create, read, update, delete (CRUD) operations        |
| 🛒 Shopping Cart    | Add / remove books, update quantity, view cart        |
| 🧾 Orders           | Checkout and order processing with stock update       |
| 📧 Notifications    | Email notifications using FastAPI Background Tasks    |
| 🔍 Search & Filters | Search books by title, author, price, or availability |
| 🗂 Modular Design   | Clean architecture with services & dependencies       |
| 🧪 Testing          | `pytest` support with sample test cases               |

---

## 📁 Project Structure

```
online_bookstore/
├── app/
│   ├── __init__.py
│   ├── main.py               # Entry point of the API
│   ├── database.py           # Database connection & session management
│   ├── models.py             # SQLAlchemy ORM models (User, Book, Author, Orders...)
│   ├── schemas.py            # Pydantic schemas for request/response validation
│   ├── crud.py               # CRUD operations and DB helper functions
│   ├── auth.py               # JWT authentication, password hashing, login/signup
│   ├── dependencies.py       # Dependency injection modules
│   ├── exceptions.py         # Custom error handlers and HTTP exceptions
│   └── utils.py              # Helper utilities (email service, token helpers, etc.)
├── tests/
│   ├── __init__.py
│   ├── test_api.py           # API test cases using pytest
│   └── conftest.py           # Fixtures for test DB and test clients
├── requirements.txt          # Project dependencies
└── README.md                 # Documentation
```

---

## 🛠️ Tech Stack

* **Python 3.10+**
* **FastAPI**
* **SQLAlchemy**
* **Pydantic**
* **JWT (JSON Web Tokens)**
* **PostgreSQL / SQLite**
* **Pytest**
* **Uvicorn**

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
[git clone https://github.com/your-username/online_bookstore.git](https://github.com/MasteriNeuron/Bookstore-api.git)
cd Bookstore-api
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment

Create a `.env` file in the project root:

```
DATABASE_URL=sqlite:///./bookstore.db
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
```

---

## ▶️ Run the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

### Access API UI Documentation

FastAPI automatically provides docs:

| URL                                                        | Type       |
| ---------------------------------------------------------- | ---------- |
| [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)   | Swagger UI |
| [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) | ReDoc      |

---


## 📌 Future Enhancements (Optional Roadmap)

* Payment gateway integration
* Recommendation engine for books
* Support for multiple sellers
* Mobile-optimized GraphQL API
* AI-based personalization

---

## 🤝 Contributing

Contributions are always welcome!
Feel free to open issues or submit pull requests to improve the project.

---

## 🪪 License

This project is licensed under the **MIT License** — free for personal and commercial use.

---

