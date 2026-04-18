# Edura / College Connect

## Project Overview
This project is a full-stack application designed for connecting college students and managing educational resources. 

The application is built using a modern decoupled architecture split into three main components:
1. **Frontend (Flutter)**: A cross-platform mobile and web application located in the `Flutter/` directory.
2. **Main Backend (Django)**: A Python-based Django server with a local SQLite database (`db.sqlite3`) located in the `Web/collegeconnect` directory. Handles user management, authentication, and core data.
3. **AI Service (Flask)**: A specialized Python service for text summarization located in the same `Web/collegeconnect` directory (`summarization_service.py`).

---

## 🚀 How to Run the Project

Follow these step-by-step instructions to run the application on your local machine.

### Prerequisites
Before you begin, ensure you have the following installed:
- [Python 3.8+](https://www.python.org/downloads/)
- [Flutter SDK](https://docs.flutter.dev/get-started/install)
- Google Chrome (for web testing) or an Android Emulator.

---

### Step 1: Install Dependencies
Navigate to the backend directory and install all required Python packages:
```bash
cd Web/collegeconnect
pip install -r requirements.txt
```

---

### Step 2: Start the Backend Services
You need to run **both** the Django server and the AI service.

#### A. Start Django Backend
In one terminal window:
```bash
cd Web/collegeconnect
python manage.py migrate
python manage.py runserver
```
> [!NOTE]
> The server typically runs at `http://127.0.0.1:8000/`. Keep this terminal open!

#### B. Start AI Summarization Service
In a **Second** terminal window:
```bash
cd Web/collegeconnect
python summarization_service.py
```
> [!NOTE]
> The AI service runs at `http://127.0.0.1:5000/`. This is required for the summarization features to work.

---

### Step 3: Start the Frontend App (Flutter)

In a **Third** terminal window:
1. Navigate to the Flutter directory:
   ```bash
   cd Flutter
   ```
2. Fetch the Flutter packages:
   ```bash
   flutter pub get
   ```
3. Run the application:
   ```bash
   flutter run -d chrome
   ```

---

## 🔐 Test Credentials

Use the following accounts to test the different roles in the application:

| Role | Username | Password |
| :--- | :--- | :--- |
| **Admin** | `sreya` | `admin123` |
| **Faculty** | `faculty.smith` | `faculty123` |
| **Student** | `student.john` | `student123` |

---

### 💡 Troubleshooting Common Issues
- **“Flutter failed to delete a directory at build\...”**: If you receive this error on Windows, it is almost entirely because OneDrive is aggressively trying to sync the `build` folder. To fix this, manually run `flutter clean` in the Flutter directory or temporarily pause your OneDrive synchronization while developing.
- **Connection Refused**: Ensure both Python services (Django on port 8000 and Flask on port 5000) are running.
