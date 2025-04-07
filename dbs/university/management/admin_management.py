import mysql.connector
from mysql.connector import Error
from datetime import datetime

class AdminDB:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',  # Add your MySQL password here
                database='university_db'
            )
            self.cursor = self.connection.cursor()
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def add_student(self, username, password, first_name, last_name, email, department_id=None, phone=None, address=None):
        try:
            # First, create user account
            user_query = """
            INSERT INTO Users (username, password, first_name, last_name, email, role, phone, address)
            VALUES (%s, %s, %s, %s, %s, 'Student', %s, %s)
            """
            self.cursor.execute(user_query, (username, password, first_name, last_name, email, phone, address))
            user_id = self.cursor.lastrowid

            # Then, create student record
            student_query = """
            INSERT INTO Students (user_id, department_id, enrollment_date, status)
            VALUES (%s, %s, %s, 'Active')
            """
            self.cursor.execute(student_query, (user_id, department_id, datetime.now().date()))
            
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error adding student: {e}")
            return False

    def get_all_students(self):
        try:
            query = """
            SELECT s.student_id, u.first_name, u.last_name, u.email, d.department_name,
                   s.gpa, s.status, s.enrollment_date, s.graduation_date
            FROM Students s
            JOIN Users u ON s.user_id = u.user_id
            LEFT JOIN Departments d ON s.department_id = d.department_id
            ORDER BY u.last_name, u.first_name
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching all students: {e}")
            return []

    def update_student(self, student_id, department_id=None, status=None):
        try:
            updates = []
            params = []
            if department_id is not None:
                updates.append("department_id = %s")
                params.append(department_id)
            if status is not None:
                updates.append("status = %s")
                params.append(status)
            
            if not updates:
                return True

            query = f"""
            UPDATE Students 
            SET {', '.join(updates)}
            WHERE student_id = %s
            """
            params.append(student_id)
            
            self.cursor.execute(query, tuple(params))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error updating student: {e}")
            return False

    def get_departments(self):
        try:
            query = "SELECT department_id, department_name FROM Departments ORDER BY department_name"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching departments: {e}")
            return []

    def close(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

# Example usage:
if __name__ == "__main__":
    db = AdminDB()
    
    # Add a new student
    db.add_student(
        username='newstudent',
        password='newstudent1234',
        first_name='New',
        last_name='Student',
        email='newstudent@university.edu',
        department_id=1,
        phone='123-456-7921',
        address='Student Dorm 21'
    )
    
    # Get all students
    all_students = db.get_all_students()
    print("All Students:", all_students)
    
    # Update a student
    db.update_student(1, department_id=2, status='Inactive')
    
    # Get all departments
    departments = db.get_departments()
    print("All Departments:", departments)
    
    db.close() 