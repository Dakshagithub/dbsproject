import mysql.connector
from mysql.connector import Error
from datetime import datetime

class StudentDB:
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

    def get_student_info(self, student_id):
        try:
            query = """
            SELECT u.first_name, u.last_name, u.email, d.department_name,
                   s.gpa, s.status, s.enrollment_date, s.graduation_date
            FROM Students s
            JOIN Users u ON s.user_id = u.user_id
            LEFT JOIN Departments d ON s.department_id = d.department_id
            WHERE s.student_id = %s
            """
            self.cursor.execute(query, (student_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching student info: {e}")
            return None

    def get_student_courses(self, student_id):
        try:
            query = """
            SELECT c.course_name, c.course_code, e.grade, e.semester, e.year
            FROM Enrollments e
            JOIN Courses c ON e.course_id = c.course_id
            WHERE e.student_id = %s
            ORDER BY e.year, e.semester
            """
            self.cursor.execute(query, (student_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching student courses: {e}")
            return []

    def update_student_info(self, student_id, status=None, gpa=None, graduation_date=None):
        try:
            updates = []
            params = []
            if status is not None:
                updates.append("status = %s")
                params.append(status)
            if gpa is not None:
                updates.append("gpa = %s")
                params.append(gpa)
            if graduation_date is not None:
                updates.append("graduation_date = %s")
                params.append(graduation_date)
            
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
            print(f"Error updating student info: {e}")
            return False

    def get_academic_summary(self, student_id):
        try:
            query = """
            SELECT 
                COUNT(DISTINCT e.course_id) as total_courses,
                AVG(CASE 
                    WHEN e.grade = 'A' THEN 4.0
                    WHEN e.grade = 'A-' THEN 3.7
                    WHEN e.grade = 'B+' THEN 3.3
                    WHEN e.grade = 'B' THEN 3.0
                    WHEN e.grade = 'B-' THEN 2.7
                    WHEN e.grade = 'C+' THEN 2.3
                    WHEN e.grade = 'C' THEN 2.0
                    WHEN e.grade = 'C-' THEN 1.7
                    WHEN e.grade = 'D+' THEN 1.3
                    WHEN e.grade = 'D' THEN 1.0
                    WHEN e.grade = 'F' THEN 0.0
                END) as gpa,
                COUNT(CASE WHEN e.grade IN ('A', 'A-') THEN 1 END) as a_grades,
                COUNT(CASE WHEN e.grade IN ('B+', 'B', 'B-') THEN 1 END) as b_grades,
                COUNT(CASE WHEN e.grade IN ('C+', 'C', 'C-') THEN 1 END) as c_grades,
                COUNT(CASE WHEN e.grade IN ('D+', 'D') THEN 1 END) as d_grades,
                COUNT(CASE WHEN e.grade = 'F' THEN 1 END) as f_grades
            FROM Enrollments e
            WHERE e.student_id = %s AND e.grade IS NOT NULL
            """
            self.cursor.execute(query, (student_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching academic summary: {e}")
            return None

    def get_current_semester_courses(self, student_id):
        try:
            current_year = datetime.now().year
            current_month = datetime.now().month
            current_semester = 'Fall' if 8 <= current_month <= 12 else 'Spring'
            
            query = """
            SELECT c.course_name, c.course_code, e.grade
            FROM Enrollments e
            JOIN Courses c ON e.course_id = c.course_id
            WHERE e.student_id = %s AND e.year = %s AND e.semester = %s
            """
            self.cursor.execute(query, (student_id, current_year, current_semester))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching current semester courses: {e}")
            return []

    def get_attendance_history(self, student_id):
        try:
            query = """
            SELECT e.semester, e.year, s.attendance_percentage
            FROM Enrollments e
            JOIN Students s ON e.student_id = s.student_id
            WHERE e.student_id = %s
            GROUP BY e.semester, e.year
            ORDER BY e.year, e.semester
            """
            self.cursor.execute(query, (student_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching attendance history: {e}")
            return []

    def close(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection closed")

# Example usage:
if __name__ == "__main__":
    db = StudentDB()
    
    # Get student information
    student_info = db.get_student_info(1)
    print("Student Information:", student_info)
    
    # Get student's courses
    student_courses = db.get_student_courses(1)
    print("Student Courses:", student_courses)
    
    # Get academic summary
    academic_summary = db.get_academic_summary(1)
    print("Academic Summary:", academic_summary)
    
    # Get current semester courses
    current_courses = db.get_current_semester_courses(1)
    print("Current Semester Courses:", current_courses)
    
    # Get attendance history
    attendance_history = db.get_attendance_history(1)
    print("Attendance History:", attendance_history)
    
    db.close() 