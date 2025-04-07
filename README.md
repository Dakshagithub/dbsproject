# University Management System

A comprehensive Django-based web application for managing university operations, including student, faculty, course, and department management.

## Features

- **User Management**
  - Multiple user roles (Admin, Student, Faculty)
  - Secure authentication system
  - User profiles with detailed information

- **Student Management**
  - Student registration and profiles
  - Course enrollment
  - GPA tracking
  - Attendance monitoring
  - Academic status tracking

- **Faculty Management**
  - Faculty profiles
  - Department assignments
  - Research project tracking
  - Course assignments

- **Course Management**
  - Course creation and scheduling
  - Prerequisite tracking
  - Semester and year management
  - Credit system

- **Department Management**
  - Department creation and organization
  - Budget tracking
  - Faculty assignments
  - Course offerings

- **Research Management**
  - Research project tracking
  - Faculty research assignments
  - Project status monitoring
  - Funding tracking

## Prerequisites

- Python 3.x
- MySQL Server
- Django 4.x
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd university-management
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure MySQL:
   - Create a database named `university_db`
   - Update database settings in `settings.py`

5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Populate initial data:
   ```bash
   python university/management/populate_db.py
   ```

## Usage

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Access the application:
   - Admin Interface: http://localhost:8000/admin/
   - User Login: http://localhost:8000/login/

3. Default credentials:
   - Admin: username: `admin`, password: `admin123`
   - Students: username: `<username>`, password: `arya1234`

## Project Structure

```
university/
├── management/
│   ├── commands/
│   ├── populate_db.py
│   └── update_students.py
├── migrations/
├── templates/
│   └── university/
│       ├── base.html
│       ├── dashboard.html
│       ├── login.html
│       ├── register.html
│       └── profile.html
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── urls.py
└── views.py
```

## Database Schema

The system uses the following main models:
- User (AbstractUser)
- Department
- Course
- Student
- Faculty
- Enrollment
- ResearchProject
- FacultyResearch

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please contact the development team or create an issue in the repository.

## Acknowledgments

- Django Framework
- MySQL Database
- Bootstrap for UI components 
