# EAC Canteen Connect

A Django-based web application designed to streamline canteen interactions at EAC, allowing students and staff to report concerns, rate food stalls, and provide suggestions.

## 🚀 Features

- **User Authentication**: Secure login and registration for students and staff.
- **Dashboard (Admin Only)**: Activity feed showing recent concerns, ratings, and suggestions.
- **Reporting System**: Submit detailed reports about canteen concerns with options for anonymity.
- **Rating System**: Rate specific food stalls and provide feedback on food quality.
- **Suggestion Box**: Share ideas for improvements or new menu items.
- **Report History**: Users can track the status of their submitted concerns.

## 🛠️ Tech Stack

- **Backend**: Python, Django
- **Frontend**: HTML, Glassmorphism-inspired CSS
- **Database**: SQLite (default)

## 📁 Project Structure

```text
eac_canteen_connect/
├── canteen/                # Main application logic
│   ├── static/             # CSS and static assets
│   ├── templates/          # HTML templates
│   ├── models.py           # Database models (Report, Rating, Suggestion, etc.)
│   ├── views.py            # Request handling and business logic
│   └── urls.py             # App-specific URL routing
├── config/                 # Project configuration (settings.py, urls.py)
├── manage.py               # Django management script
└── db.sqlite3              # Database file
```

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd eac_canteen_connect
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install django pillow
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## 📝 Stall Choices

The following stalls are currently supported:

- Maren's Food Cart
- Rhoxy Canteen
- M.D Mangubat Canteen
- Stall 4
- Goldfranz Canteen
- K-Pop House
- kCairo Johns Food Hub
- Tiger Crunch
