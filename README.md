# Culture Connect – Final Project

A web application that allows users to share stories, proverbs, dishes, tourist attractions, and cultural insights from around the world. Users can post content, edit/delete their own posts, explore global posts, filter by country and category, and save favorite posts using localStorage.

---

## New Feature Implemented

**Favorite Posts System** – Users can save posts locally using the browser's localStorage, and the UI highlights saved favorites instantly.

---

## Prerequisites

**Modules to install:**

```bash
pip install flask

Other functions rely on Python's built‑in modules only: `json`, `re`, `os`.

---

## Project Structure

culture_connect/
│
├── app.py
├── db/
│   ├── users.json
│   └── posts.json
├── README.md
└── website/
    ├── __init__.py
    ├── auth.py
    ├── models.py
    ├── views.py
    ├── shared.py
    ├── validators.py
    ├── post_service.py
    ├── static/
    │   ├── css/
    │   ├── js/
    |   ├── images/
    │   └── uploads/
    └── templates/
        ├── base.html
        ├── profile.html
        ├── global_posts.html
        ├── card.html
        ├── signup.html
        ├── login.html
        ├── index.html
        └── post_modal.html

---

## Run Locally

1. Clone the repository:

```bash
git clone https://github.com/sandymosaad/culture_connect.git
cd culture_connect
```

2. Set Flask environment and run server:

```bash
# Windows
set FLASK_APP=app.py
set FLASK_ENV=development
flask run

# Linux / Mac
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

3. Open your browser at:

  http://127.0.0.1:5000

---

## Project Checklist

### Backend (Python / Flask)

* [x] Uses Flask web framework.
* [x] Reads and writes to JSON files (`users.json`, `posts.json`).
* [x] Contains class `Post` with properties and methods.

  * File: `models.py`
  * Line: 4
  * Properties: `title`, `body`
  * Methods: `to_dict()`, `get_user_posts()`
  * Usage: `views.py` lines 70 & 73

### Frontend (HTML / CSS / JS)

* [x] Custom CSS styling.
* [x] JavaScript with modern syntax (`let`, `const`).
* [x] Uses `localStorage` for saving favorite posts.

### User Input / Validation

* [x] Users can enter title, body, category for posts.
* [x] Input is validated in backend (`valid_post_data`, `valid_sign_up_data`).
* [x] Friendly error messages are shown if input is invalid.
* [x] No unhandled error messages are displayed to users.

### Loops & Conditionals

* Loops:

  * File: `profile.html`
  * Lines: 14–19

  jinja2
  {% for post in posts %}
  
* Conditionals:

  * File: `signup.html`
  * Lines: 15–17

  jinja2
  {% if errors.username_error %}
  
---

## Summary of Features

* User authentication (signup/login/logout)
* Create/Edit/Delete posts
* Upload images for posts and profile
* Display global posts with filtering by country and category
* Save favorite posts locally using `localStorage`
* Data validation for inputs (title, body, username, email, country, password)
* Uses classes in backend for better structure (`Post` & `User` )

---

## GitHub Repository

[Culture Connect Repository](https://github.com/sandymosaad/culture_connect)
