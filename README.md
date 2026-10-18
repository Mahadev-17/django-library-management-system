# Library Management System (Django)

## Features
- Admin login/logout
- Dashboard summary
- Book and student CRUD
- Search books and students
- Issue and return books
- Overdue tracking and a simple ₹5/day fine calculation
- Django admin panel
- SQLite for local development

## Run locally (Windows PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations books
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/ and log in with the superuser account.

## GitHub
Before pushing, check `.gitignore`. Do not commit `db.sqlite3`, virtual environments, passwords, or production secret keys.

## PythonAnywhere deployment outline
1. Push the project to a GitHub repository.
2. On PythonAnywhere, open a Bash console and clone the repository.
3. Create a virtual environment using a Python version supported by your account, then install requirements.
4. In the Web tab, create a manual-configured web app using the same Python version.
5. Set the virtualenv path and edit the WSGI file to import `application` from this project's `library.wsgi`.
6. Configure environment variables or production settings: `DJANGO_DEBUG=0`, a strong `DJANGO_SECRET_KEY`, and `DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com`.
7. Run migrations, create a superuser, set up static files (`collectstatic`), configure the static files mapping in the Web tab, and reload the web app.
8. Test login, adding books/students, issue/return, and search.

## Important
This starter project is intended for learning. Review security, backups, and production settings before using it with real student data.
