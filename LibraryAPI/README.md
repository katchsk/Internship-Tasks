# LibraryAPI

A Django REST Framework (DRF) project with JWT authentication, book and review management, and interactive API documentation via Swagger.

---

## Features
- User registration & JWT authentication  
- Book CRUD (Create, Read, Update, Delete)  
- Add and list reviews for books  
- Swagger API docs at `/swagger/`  
- Fully tested with `pytest`  

---

## Setup

### 1. Clone repository
git clone https://github.com/yourusername/LibraryAPI.git
cd LibraryAPI

### 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

### 3. Install dependencies
pip install -r requirements.txt

### 4. Environment variables
Create a .env file in the project root:
SECRET_KEY=your_secret_key_here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

### 5. Apply migrations 
python manage.py migrate

### 6. Run server
python manage.py runserver

## Authentication
This project uses JWT.

### Register:
POST /users/api/auth/register/

#### Body:
{
  "username": "newuser",
  "password": "password123"
}

### Login (to get tokens):

POST /users/api/auth/login/

#### Body:
{
  "username": "newuser",
  "password": "password123"
}

#### Response:
{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}
#### Use the access token in headers:
Authorization: Bearer <access_token>

## 📘 Endpoints
### Users
POST /users/api/auth/register/ → Register new user

POST /users/api/auth/login/ → Obtain JWT tokens

### Books
GET /api/books/ → List all books

POST /api/books/ → Create new book (auth required)

GET /api/books/{id}/ → Get book details

PUT /api/books/{id}/ → Update book (auth required)

DELETE /api/books/{id}/ → Delete book (auth required)

### Reviews
GET /api/books/{book_id}/reviews/ → List reviews for a book

POST /api/books/{book_id}/reviews/add/ → Add review (auth required)

## API Documentation
Interactive Swagger docs available at:
/swagger/

## Testing
Make sure you have pytest-django installed

Run unit tests with:
pytest -v

All tests should pass:
5 passed in X.XXs

## 📄 License
This project is licensed under the BSD License.