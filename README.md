# Edura 🎓

A full-stack application for college resource management and student connectivity.

## 🚀 Quick Start

### 1. Main Backend (Django)
```bash
cd Web/collegeconnect
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 2. AI Service (Flask)
*Required for summarization features.*
```bash
cd Web/collegeconnect
python summarization_service.py
```

### 3. Frontend (Flutter)
```bash
cd Flutter
flutter pub get
flutter run -d chrome
```

---

## 🔐 Test Credentials

| Role | Username | Password |
| :--- | :--- | :--- |
| **Admin** | `sreya` | `admin123` |
| **Faculty** | `faculty.smith` | `faculty123` |
| **Student** | `student.john` | `student123` |

---

## 💡 Troubleshooting
* **Build Errors?** Run `flutter clean` in the `Flutter` folder.
* **Service Connection?** Ensure **both** Django (port 8000) and AI (port 5000) are running.
* **OneDrive Issues?** Pause syncing if the Flutter build directory is locked.
