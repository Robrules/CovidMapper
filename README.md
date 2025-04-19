# COVID Mapper

A web app that visualises COVID‑19 risk by NSW Local Government Area (LGA), lets you bookmark locations and stay informed via an interactive Mapbox map.

---

## ✨ Features
- **Real-time data** from the NSW Health API (case counts & vaccination rates)  
- **Risk engine** (`determineRisk()`) assigns colour‑coded risk levels per LGA  
- **Interactive map** with Mapbox geocoder search and LGA boundary layers  
- **User accounts** (Django auth): registration, email confirmation, login/logout  
- **Bookmarking**: create lists of LGAs you want to monitor  
- **Offline cache** via SQLite (optional)  

---

## 🚀 Setup

1. **Clone & venv**  
   ```bash
   git clone <repo-url>
   cd covid-mapper
   pip install virtualenv
   python -m venv .\covid_mapper\venv
   ./venv/Scripts/activate      # Windows
   source ./venv/bin/activate   # macOS/Linux
   ```
2. **Install deps**  
   ```bash
   pip install -r requirements.txt
   npm install vue bootstrap bootstrap-vue
   ```
3. **Migrate**  
   ```bash
   python manage.py makemigrations system
   python manage.py migrate
   ```
4. **Run**  
   ```bash
   python manage.py runserver
   ```

---

## 🧪 Testing

- **Unit tests** for registration, login, list & location management  
- **Integration tests** cover API endpoints and DB models  
- Run coverage:  
  ```bash
  coverage run manage.py test
  coverage report
  ```

---

## 🛠 Tech stack

| Layer    | Tools & Libraries                     |
|----------|---------------------------------------|
| Backend  | Django, Django REST Framework, SQLite (ORM) |
| Frontend | Vue.js, Axios, Bootstrap‑Vue, Mapbox GL JS |
| Testing  | unittest, coverage                    |

---

## 🎯 Impact

- Helped friends & family monitor LGA‑level COVID risk during lockdown  
- Demonstrates end‑to‑end API integration, real‑time data handling, mapping and user auth  

---

> _Originally built as a project for Software Design._
