<div align="center">

<h1>Manpower Supply Agency</h1>

<p>An ERP for Manpower Supply Agency to Manage Agent, Passengers, Accounts, Company Cost, Company Documents and Tracking Passenger Status.</p>

<br>

<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green">
<img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white">
<img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white">
<img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white">
<img src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white">
<img src="https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4">
<img src="https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white">
<img src="https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=Cloudflare&logoColor=white">
<img src="https://img.shields.io/badge/Railway-131415?style=for-the-badge&logo=railway&logoColor=white">

<br>

<p>
<b><a href="https://manpower-supply-agency.musfiqdehan.com">Live Site</a></b>
</p>

<p>
<b><a href="https://hub.docker.com/r/musfiqdehan/manpower-supply-agency-erp">Docker Image</a></b>
</p>

</div>


### Table of Contents
- [Technology Used](#technology-used)
- [Features](#features)
- [Advanced Features](#advanced-features)
- [Advanced Configuration](#advanced-configuration)
- [Running Locally using Git](#running-locally-using-git)
- [Running Locally using Docker](#running-locally-using-docker)
- [Configuration](#configuration)
- [SetUp Environment Variables](#setup-environment-variables)


### Technology Used

-   **Frontend:** HTML5, CSS3, Bootstrap5
-   **Backend:** Python=3.11.10, Django=5.1.1
-   **Database:** PostgreSQL
-   **Version Control:** Git, GitHub, GitLab
-   **Containerization:** Docker
-   **Background Task Manage:** Redis, Celery, Supervisor
-   **Editor:** VS Code
-   **Operating System:** Ubuntu 24.04 LTS
-   **Browser(Tested On):** Google Chrome, Microsoft Edge, Mozilla Firefox


### Features

- **Dashboard:** Display the summary of the application.
- **Agent Management:** Add, Update, Delete, List, Search, Filter, Export Agents.
- **Passenger Management:** Add, Update, Delete, List, Search, Filter, Export Passengers.
- **Company Cost Management:** Add, Update, Delete, List, Search, Filter, Export Company Cost.
- **Company Document Management:** Add, Update, Delete, List, Search, Filter, Export Company Documents.
- **Passenger Status Management:** Add, Update, Delete, List, Search, Filter, Export Passenger Status.
- **Notification:** Send notification before document expiry date.
- **User Management:** Add, Update, Delete, List, Search, Filter, Export Users.
- **Group/Role Management:** Add, Update, Delete, List Roles.
- **Permission Management:** Add, Update, Delete Permissions.


### Advanced Features

- Use Django's Decorators to restrict access to views based on user roles and permissions.
- Use Django's Context Processor to add custom Notification context to all templates.
- Build custom UserManager and Permissions to manage user roles/groups and permissions.


### Advanced Configuration

- Use PostgreSQL for database. Use railway for hosting cloud database.
- Use celery for background task management. To create notification before document expiry date.
- Use AWS S3 for storing static and media files.
- Use Cloudflare for CDN.
- Use Docker for containerization.
- Use `supervisor` for managing celery worker and beat.
- Use Docker to run the application and deploy it in the railway.app to host the application.



### Running Locally using Git

1. **Clone the repository:**
   ```bash
   git clone https://github.com/musfiqdehan/OnlineLearningPlatform.git
   cd your-project
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
    ```
Now visit `http://127.0.0.1:8000/` in your web browser to see the application in action.


### Running Locally using Docker

- Pull the Docker Image

```bash
docker pull musfiqdehan/manpower-supply-agency-erp:latest
```

- Run using Docker

```bash
docker run -p 8080:8080 musfiqdehan/manpower-supply-agency-erp:latest

```
- Run using Docker Compose

```bash
docker-compose up --build
```

### Configuration

There is separate settings for production and development server. Below is the folder structure of my project folder

```
.
├── asgi.py
├── celery.py
├── __init__.py
├── mysitemap.py
├── settings
│   ├── base.py
│   ├── development.py
│   ├── __init__.py
│   └── production.py
├── urls.py
└── wsgi.py

```

### SetUp Environment Variables

- Create a `.env` file in the root of the project folder and add the following environment variables

- See the `.env.example` file for reference

```
SECRET_KEY=
DJANGO_SETTINGS_MODULE=

# AWS S3 settings for production
AWS_STORAGE_BUCKET_NAME=
AWS_LOCATION=
AWS_S3_ACCESS_KEY_ID=
AWS_S3_SECRET_ACCESS_KEY=
AWS_S3_CUSTOM_DOMAIN=
AWS_S3_ENDPOINT_URL=
AWS_S3_FILE_OVERWRITE=

# Database settings for production
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# Celery settings for production
CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=
```
