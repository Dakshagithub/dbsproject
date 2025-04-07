from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import User, Student, Faculty

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=[
        ('Student', 'Student'),
        ('Faculty', 'Faculty'),
    ])
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role', 'phone', 'address')

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['enrollment_date', 'status', 'gpa', 'graduation_date']
        widgets = {
            'enrollment_date': forms.DateInput(attrs={'type': 'date'}),
            'graduation_date': forms.DateInput(attrs={'type': 'date'}),
        }

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['hire_date', 'title', 'specialization', 'salary', 'office_location']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        } 