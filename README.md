#  Task Manager

It allows you to create tasks, assign statuses, attach labels, and manage them through a web interface.  


### Hexlet tests and linter status:
[![Actions Status](https://github.com/VVP04/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/RustemYeldessov/python-project-52/actions)


## 🚀 Deployment  
The project is deployed on [Render](https://render.com):  
👉 [Task Manager Demo](https://python-project-52-au35.onrender.com) 


## ⚙️ Technologies
- [Python 3.11+](https://www.python.org/)  
- [Django 5](https://www.djangoproject.com/)  
- [PostgreSQL](https://www.postgresql.org/) (production)  
- [Bootstrap 5](https://getbootstrap.com/)  
- [django-filter](https://django-filter.readthedocs.io/)  
- [Whitenoise](http://whitenoise.evans.io/) for static files  
- [Rollbar](https://rollbar.com/) for error monitoring  

## 📦 Installation & Local Development

```bash

git clone https://github.com/RustemYeldessov/python-project-52
cd task-manager
```
### Create virtual environment
```bash

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### Install dependencies
```bash

pip install -r requirements.txt
```

### Run migrations
```bash

python manage.py migrate
```
### Start dev server
```bash

python manage.py runserver
```