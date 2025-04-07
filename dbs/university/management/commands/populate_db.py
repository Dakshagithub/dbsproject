from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from university.models import User, Student, Faculty, Department, Course, Enrollment, ResearchProject, FacultyResearch

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        # Create departments
        cs_dept = Department.objects.create(
            department_name='Computer Science',
            department_code='CS',
            budget=1000000.00,
            established_year=1990,
            description='Department of Computer Science'
        )

        math_dept = Department.objects.create(
            department_name='Mathematics',
            department_code='MATH',
            budget=800000.00,
            established_year=1985,
            description='Department of Mathematics'
        )

        # Create courses
        cs101 = Course.objects.create(
            course_name='Introduction to Programming',
            course_code='CS101',
            department=cs_dept,
            credits=3,
            description='Basic programming concepts',
            semester='Fall',
            year=2024
        )

        math101 = Course.objects.create(
            course_name='Calculus I',
            course_code='MATH101',
            department=math_dept,
            credits=4,
            description='Introduction to calculus',
            semester='Fall',
            year=2024
        )

        # Create admin user
        admin = User.objects.create(
            username='admin',
            email='admin@university.edu',
            password=make_password('admin1234'),
            role='Admin',
            first_name='John',
            last_name='Smith',
            phone='1234567890',
            address='123 Admin St, University City'
        )

        # Create faculty users
        faculty_data = [
            {
                'username': 'jdoe',
                'email': 'jdoe@university.edu',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'department': cs_dept,
                'title': 'Professor',
                'specialization': 'Artificial Intelligence'
            },
            {
                'username': 'rjohnson',
                'email': 'rjohnson@university.edu',
                'first_name': 'Robert',
                'last_name': 'Johnson',
                'department': math_dept,
                'title': 'Associate Professor',
                'specialization': 'Applied Mathematics'
            }
        ]

        for data in faculty_data:
            user = User.objects.create(
                username=data['username'],
                email=data['email'],
                password=make_password(f"{data['username']}1234"),
                role='Faculty',
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone='1234567890',
                address='Faculty Housing, University City'
            )
            
            Faculty.objects.create(
                user=user,
                department=data['department'],
                title=data['title'],
                specialization=data['specialization'],
                hire_date=timezone.now().date(),
                salary=80000.00,
                office_location=f"Building {data['department'].department_code}, Room 101"
            )

        # Create student users
        student_data = [
            {
                'username': 'asmith',
                'email': 'asmith@university.edu',
                'first_name': 'Alice',
                'last_name': 'Smith',
                'department': cs_dept,
                'course': cs101,
                'gpa': 3.8
            },
            {
                'username': 'bwilson',
                'email': 'bwilson@university.edu',
                'first_name': 'Bob',
                'last_name': 'Wilson',
                'department': math_dept,
                'course': math101,
                'gpa': 3.5
            }
        ]

        for data in student_data:
            user = User.objects.create(
                username=data['username'],
                email=data['email'],
                password=make_password(f"{data['username']}1234"),
                role='Student',
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone='1234567890',
                address='Student Dormitory, University City'
            )
            
            student = Student.objects.create(
                user=user,
                department=data['department'],
                course=data['course'],
                enrollment_date=timezone.now().date(),
                graduation_date=timezone.now().date().replace(year=timezone.now().year + 4),
                gpa=data['gpa'],
                status='Active'
            )

            # Create enrollments
            Enrollment.objects.create(
                student=student,
                course=data['course'],
                enrollment_date=timezone.now().date(),
                semester='Fall',
                year=2024,
                grade='A'
            )

        # Create research projects
        research_projects = [
            {
                'title': 'Machine Learning Applications',
                'description': 'Research on ML applications in healthcare',
                'department': cs_dept,
                'faculty': Faculty.objects.get(user__username='jdoe')
            },
            {
                'title': 'Mathematical Modeling',
                'description': 'Advanced mathematical modeling techniques',
                'department': math_dept,
                'faculty': Faculty.objects.get(user__username='rjohnson')
            }
        ]

        for project_data in research_projects:
            project = ResearchProject.objects.create(
                title=project_data['title'],
                description=project_data['description'],
                start_date=timezone.now().date(),
                end_date=timezone.now().date().replace(year=timezone.now().year + 2),
                funding=50000.00,
                status='Active',
                department=project_data['department']
            )
            
            FacultyResearch.objects.create(
                faculty=project_data['faculty'],
                project=project,
                role='Principal Investigator'
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample data')) 