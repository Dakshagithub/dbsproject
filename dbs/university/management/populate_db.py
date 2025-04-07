import mysql.connector
from mysql.connector import Error
from datetime import datetime
from werkzeug.security import generate_password_hash

def populate_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='university_db',
            consume_results=True  # Add this to handle multiple queries
        )
        cursor = connection.cursor(buffered=True)  # Use buffered cursor

        # Create admin user if not exists
        admin_query = """
        INSERT INTO Users (username, email, password, first_name, last_name, role)
        SELECT 'admin', 'admin@university.edu', %s, 'Admin', 'User', 'admin'
        WHERE NOT EXISTS (SELECT 1 FROM Users WHERE username = 'admin')
        """
        # Django's default password hasher format
        admin_password = 'admin123'
        cursor.execute(admin_query, (admin_password,))

        # Create departments
        departments = [
            ('Computer Science', 'CS'),
            ('Mathematics', 'MATH'),
            ('Physics', 'PHYS'),
            ('Engineering', 'ENG')
        ]
        
        for dept_name, dept_code in departments:
            dept_query = """
            INSERT IGNORE INTO Departments (department_name, department_code)
            VALUES (%s, %s)
            """
            cursor.execute(dept_query, (dept_name, dept_code))

        # Create sample students
        students = [
            {
                'username': 'jsmith',
                'email': 'jsmith@university.edu',
                'password': generate_password_hash('arya1234'),
                'first_name': 'John',
                'last_name': 'Smith',
                'department': 'Computer Science',
                'gpa': 3.5,
                'status': 'Active'
            },
            {
                'username': 'mjohnson',
                'email': 'mjohnson@university.edu',
                'password': generate_password_hash('arya1234'),
                'first_name': 'Mary',
                'last_name': 'Johnson',
                'department': 'Mathematics',
                'gpa': 3.8,
                'status': 'Active'
            },
            {
                'username': 'rwilliams',
                'email': 'rwilliams@university.edu',
                'password': generate_password_hash('arya1234'),
                'first_name': 'Robert',
                'last_name': 'Williams',
                'department': 'Physics',
                'gpa': 3.6,
                'status': 'Active'
            },
            {
                'username': 'sbrown',
                'email': 'sbrown@university.edu',
                'password': generate_password_hash('arya1234'),
                'first_name': 'Sarah',
                'last_name': 'Brown',
                'department': 'Engineering',
                'gpa': 3.9,
                'status': 'Active'
            },
            {
                'username': 'dlee',
                'email': 'dlee@university.edu',
                'password': generate_password_hash('arya1234'),
                'first_name': 'David',
                'last_name': 'Lee',
                'department': 'Computer Science',
                'gpa': 3.7,
                'status': 'Active'
            },
            {
                'username': 'agarcia',
                'email': 'agarcia@university.edu',
                'password': generate_password_hash('arya1234'),
                'first_name': 'Ana',
                'last_name': 'Garcia',
                'department': 'Mathematics',
                'gpa': 3.4,
                'status': 'Active'
            },
            {
                'username': 'mwilson',
                'email': 'mwilson@university.edu',
                'password': generate_password_hash('arya1234'),
                'first_name': 'Michael',
                'last_name': 'Wilson',
                'department': 'Physics',
                'gpa': 3.2,
                'status': 'Active'
            },
            {
                'username': 'janderson',
                'email': 'janderson@university.edu',
                'password': generate_password_hash('arya1234'),
                'first_name': 'Jennifer',
                'last_name': 'Anderson',
                'department': 'Engineering',
                'gpa': 3.8,
                'status': 'Active'
            }
        ]

        for student in students:
            # Get department ID
            cursor.execute("SELECT department_id FROM Departments WHERE department_name = %s", 
                         (student['department'],))
            dept_result = cursor.fetchone()
            if not dept_result:
                continue

            # Create user
            user_query = """
            INSERT IGNORE INTO Users (username, email, password, role, first_name, last_name)
            VALUES (%s, %s, %s, 'Student', %s, %s)
            """
            cursor.execute(user_query, (
                student['username'],
                student['email'],
                student['password'],
                student['first_name'],
                student['last_name']
            ))

            # Get user ID
            cursor.execute("SELECT user_id FROM Users WHERE username = %s", (student['username'],))
            user_result = cursor.fetchone()
            if not user_result:
                continue

            # Create student record
            student_query = """
            INSERT IGNORE INTO Students (user_id, department_id, enrollment_date, gpa, status)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(student_query, (
                user_result[0],
                dept_result[0],
                datetime.now().date(),
                student['gpa'],
                student['status']
            ))

        connection.commit()
        print("Database populated successfully!")

    except Error as e:
        print(f"Error populating database: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    populate_db() 