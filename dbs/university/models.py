from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Student', 'Student'),
        ('Faculty', 'Faculty'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

class Department(models.Model):
    department_name = models.CharField(max_length=50)
    department_code = models.CharField(max_length=10, unique=True)
    head_faculty = models.ForeignKey('Faculty', on_delete=models.SET_NULL, null=True, related_name='headed_department')
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    established_year = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.department_name

class Course(models.Model):
    course_name = models.CharField(max_length=50)
    course_code = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    credits = models.IntegerField()
    description = models.TextField()
    prerequisites = models.TextField(null=True, blank=True)
    SEMESTER_CHOICES = [
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
    ]
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    enrollment_date = models.DateField()
    graduation_date = models.DateField(null=True, blank=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Graduated', 'Graduated'),
        ('On Leave', 'On Leave'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.user.get_full_name()

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    TITLE_CHOICES = [
        ('Professor', 'Professor'),
        ('Associate Professor', 'Associate Professor'),
        ('Assistant Professor', 'Assistant Professor'),
        ('Lecturer', 'Lecturer'),
    ]
    title = models.CharField(max_length=50, choices=TITLE_CHOICES)
    specialization = models.CharField(max_length=100)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    office_location = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title} {self.user.get_full_name()}"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField()
    GRADE_CHOICES = [
        ('A', 'A'), ('A-', 'A-'),
        ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'),
        ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'),
        ('D+', 'D+'), ('D', 'D'),
        ('F', 'F'), ('W', 'W'), ('I', 'I'),
    ]
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, null=True, blank=True)
    SEMESTER_CHOICES = [
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
    ]
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    year = models.IntegerField()

    class Meta:
        unique_together = ('student', 'course', 'semester', 'year')

    def __str__(self):
        return f"{self.student} - {self.course} ({self.semester} {self.year})"

class ResearchProject(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    funding = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    faculty_members = models.ManyToManyField(Faculty, through='FacultyResearch')

    def __str__(self):
        return self.title

class FacultyResearch(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)

    class Meta:
        unique_together = ('faculty', 'project')

    def __str__(self):
        return f"{self.faculty} - {self.project} ({self.role})"
