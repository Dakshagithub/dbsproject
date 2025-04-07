import mysql.connector
from mysql.connector import Error
from datetime import datetime

def update_student_records():
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='university_db'
        )
        
        cursor = connection.cursor()
        
        # Get all student users
        cursor.execute("""
            SELECT u.user_id, u.username, u.first_name, u.last_name, u.email
            FROM Users u
            WHERE u.role = 'Student'
        """)
        student_users = cursor.fetchall()
        
        # For each student user, ensure they have a Student record
        for user in student_users:
            user_id = user[0]
            cursor.execute("""
                SELECT student_id FROM Students WHERE user_id = %s
            """, (user_id,))
            if not cursor.fetchone():
                # Create Student record if it doesn't exist
                cursor.execute("""
                    INSERT INTO Students (user_id, department_id, enrollment_date, status, gpa, attendance_percentage)
                    VALUES (%s, 1, %s, 'Active', 0.0, 100.0)
                """, (user_id, datetime.now().date()))
        
        connection.commit()
        print("Student records updated successfully!")
        
    except Error as e:
        print(f"Error updating student records: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    update_student_records() 