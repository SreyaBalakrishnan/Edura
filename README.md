Edura 

A full-stack project for college resource management and student connectivity.

to run the project 

Setup Backend
Open a terminal and run:
   cd Web/collegeconnect
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver

Start AI Service
Open a **second** terminal and run:
   ```bash
   cd Web/collegeconnect
   python summarization_service.py
   ```
Run Flutter App
Open a **third** terminal and run:
```bash
cd Flutter
flutter pub get
flutter run -d chrome
```


## 💡 Troubleshooting
* **Build Errors?** Run `flutter clean` in the Flutter folder.
* **Feature Not Working?** Ensure **both** the Django (port 8000) and AI service (port 5000) are running.
