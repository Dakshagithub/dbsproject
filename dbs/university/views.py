from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from .models import User, Student, Faculty, Course, Department, Enrollment, ResearchProject
from .forms import UserRegistrationForm, StudentForm, FacultyForm, CustomLoginForm

def index(request):
    return render(request, 'university/index.html')

def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            user.last_login = timezone.now()
            user.save()
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    return render(request, 'university/login.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                if user.role == 'Student':
                    Student.objects.create(
                        user=user,
                        enrollment_date=timezone.now().date(),
                        status='Active',
                        gpa=0.0
                    )
                elif user.role == 'Faculty':
                    Faculty.objects.create(
                        user=user,
                        hire_date=timezone.now().date(),
                        title='Assistant Professor',
                        specialization='General',
                        salary=0.0,
                        office_location='TBD'
                    )
                messages.success(request, 'Registration successful. Please log in.')
                return redirect('login')
            except Exception as e:
                user.delete()
                messages.error(request, f'Registration failed: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'university/register.html', {'form': form})

@login_required
def dashboard(request):
    context = {
        'user': request.user,
    }
    
    if request.user.role == 'Admin':
        context.update({
            'students': Student.objects.all(),
        })
    elif request.user.role == 'Student':
        try:
            student = Student.objects.get(user=request.user)
            enrollments = Enrollment.objects.filter(student=student)
            context.update({
                'student': student,
                'enrollments': enrollments,
            })
        except Student.DoesNotExist:
            # Create a Student record if it doesn't exist
            student = Student.objects.create(
                user=request.user,
                enrollment_date=timezone.now().date(),
                status='Active',
                gpa=0.0
            )
            context.update({
                'student': student,
                'enrollments': [],
            })
    elif request.user.role == 'Faculty':
        try:
            faculty = Faculty.objects.get(user=request.user)
            research_projects = ResearchProject.objects.filter(faculty_members=faculty)
            context.update({
                'faculty': faculty,
                'research_projects': research_projects,
            })
        except Faculty.DoesNotExist:
            # Create a Faculty record if it doesn't exist
            faculty = Faculty.objects.create(
                user=request.user,
                hire_date=timezone.now().date(),
                title='Assistant Professor',
                specialization='General',
                salary=0.0,
                office_location='TBD'
            )
            context.update({
                'faculty': faculty,
                'research_projects': [],
            })
    
    return render(request, 'university/dashboard.html', context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    if request.user.role == 'Student':
        student = Student.objects.get(user=request.user)
        if request.method == 'POST':
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile')
        else:
            form = StudentForm(instance=student)
        return render(request, 'university/profile.html', {'form': form})
    
    elif request.user.role == 'Faculty':
        faculty = Faculty.objects.get(user=request.user)
        if request.method == 'POST':
            form = FacultyForm(request.POST, instance=faculty)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile')
        else:
            form = FacultyForm(instance=faculty)
        return render(request, 'university/profile.html', {'form': form})
    
    return render(request, 'university/profile.html')

def is_admin(user):
    return user.role == 'Admin'

@login_required
@user_passes_test(is_admin)
def add_student(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.role = 'Student'
                user.save()
                
                student = Student.objects.create(
                    user=user,
                    enrollment_date=timezone.now().date(),
                    status='Active',
                    gpa=0.0
                )
                messages.success(request, 'Student added successfully.')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f'Error adding student: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'university/add_student.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm(instance=student)
    return render(request, 'university/edit_student.html', {'form': form, 'student': student})
