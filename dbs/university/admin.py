from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department, Course, Student, Faculty, Enrollment, ResearchProject, FacultyResearch

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role', 'phone', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name', 'department_code', 'get_head_faculty', 'budget', 'established_year')
    search_fields = ('department_name', 'department_code', 'description')
    list_filter = ('established_year',)

    def get_head_faculty(self, obj):
        return obj.head_faculty.user.get_full_name() if obj.head_faculty else 'Not assigned'
    get_head_faculty.short_description = 'Head Faculty'

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_code', 'get_department', 'credits', 'semester', 'year', 'get_prerequisites')
    search_fields = ('course_name', 'course_code', 'description')
    list_filter = ('department', 'semester', 'year', 'credits')
    ordering = ('course_code',)

    def get_department(self, obj):
        return obj.department.department_name
    get_department.short_description = 'Department'

    def get_prerequisites(self, obj):
        return obj.prerequisites if obj.prerequisites else 'None'
    get_prerequisites.short_description = 'Prerequisites'

class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_email', 'get_phone', 'get_department', 'get_course', 'gpa', 'status', 'enrollment_date', 'graduation_date', 'attendance_percentage')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'user__phone')
    list_filter = ('department', 'status', 'enrollment_date', 'course')
    ordering = ('user__last_name', 'user__first_name')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'department')
        }),
        ('Course Information', {
            'fields': ('course',)
        }),
        ('Academic Information', {
            'fields': ('enrollment_date', 'graduation_date', 'gpa', 'attendance_percentage', 'status')
        }),
    )

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_phone(self, obj):
        return obj.user.phone
    get_phone.short_description = 'Phone'

    def get_department(self, obj):
        return obj.department.department_name if obj.department else 'Not assigned'
    get_department.short_description = 'Department'

    def get_course(self, obj):
        return obj.course.course_name if obj.course else 'Not assigned'
    get_course.short_description = 'Course'

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_email', 'department', 'title', 'specialization')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'specialization')
    list_filter = ('department', 'title')

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'semester', 'year', 'grade')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'course__course_name')
    list_filter = ('semester', 'year', 'grade')

class ResearchProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'status', 'start_date', 'end_date', 'funding')
    search_fields = ('title', 'description')
    list_filter = ('department', 'status')

class FacultyResearchAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'project', 'role')
    search_fields = ('faculty__user__first_name', 'faculty__user__last_name', 'project__title')
    list_filter = ('role',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(ResearchProject, ResearchProjectAdmin)
admin.site.register(FacultyResearch, FacultyResearchAdmin)
