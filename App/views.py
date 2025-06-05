from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm, EmployeeForm
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import user_passes_test

def superuser_check(user):
    if not user.is_superuser:
        messages.error(user, "Access Denied! Only admins can view this page.")
    return user.is_superuser

# User login view

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log in the user

            # Redirect based on user type
            if user.is_superuser:
                return redirect('admin-dashboard')  # Redirect superuser to admin dashboard
            else:
                return redirect('profile')  # Redirect normal user to profile page
    else:
        form = AuthenticationForm()
    
    return render(request, 'account/login.html', {'form': form})

# User logout view
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


# User registration view
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm, EmployeeForm
from .models import Employee, Profile
import face_recognition

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import EmployeeForm

def register(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the new employee (this will also create the user and profile)
            employee = form.save()

            # Log in the user automatically after successful registration
            login(request, employee.user)

            messages.success(request, "Your account has been created successfully!")
            return redirect('profile')  # Redirect to the profile page or wherever you want
    else:
        form = EmployeeForm()

    return render(request, 'account/register.html', {'form': form})

# Profile update view
@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')  # Redirect to the profile page after update
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'account/profile.html', {'profile_form': profile_form})


@user_passes_test(lambda user: user.is_superuser, login_url='login')
def admin_profile(request):
    user = request.user
    
    # Fetch or create the Employee & Profile objects
    employee, created = Employee.objects.get_or_create(user=user)
    profile, created = Profile.objects.get_or_create(user=user)

    title = "My Profile"

    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES, instance=employee)

        if form.is_valid():
            # Update User model
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            # Update Profile model
            profile.contact = form.cleaned_data['contact']
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']  # Save new profile image
            profile.save()

            # Update Employee model
            employee = form.save(commit=False)
            employee.user = user  # Ensure correct user assignment
            employee.save()

            messages.success(request, "Profile updated successfully!")
            return redirect('admin-profile')  # Redirect back to the profile page

        else:
            messages.error(request, "Please correct the errors below.")  # Show form errors

    else:
        # Pre-fill form with existing data
        form = EmployeeForm(instance=employee, initial={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'contact': profile.contact,
        })

    return render(request, 'admin/profile.html', {'form': form, 'employee': employee, 'title': title})

@user_passes_test(lambda user: user.is_superuser, login_url='login')
def admin_dashboard(request):
    total_employees = Employee.objects.filter(status="Active").count() 
    present = 0
    absent = total_employees-present

    context = {
        'total_employees': total_employees,
        'present': present,
        'absent': absent

    }
    return render(request, 'admin/dashboard.html', context)

@user_passes_test(lambda user: user.is_superuser, login_url='login')
def employees(request):
    employees = Employee.objects.all()
    return render(request, 'admin/employees.html', {'employees': employees})


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError, transaction
from .models import Profile, Employee
from .forms import EmployeeForm

@user_passes_test(lambda user: user.is_superuser, login_url='login')
# When adding a new employee or updating an employee profile
def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)  # Handle file uploads (profile image)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            # Create Profile and Employee
            profile = Profile.objects.create(user=user, profile_image=form.cleaned_data['profile_image'])
            employee = Employee.objects.create(user=user, dep=form.cleaned_data['dep'], role=form.cleaned_data['role'],
                                               status=form.cleaned_data['status'])

            # Capture face encoding and store it in Employee model
            if form.cleaned_data['profile_image']:
                image_path = form.cleaned_data['profile_image'].path
                image = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(image)[0]
                employee.set_face_encoding(encoding)
                employee.save()

            messages.success(request, "Employee added successfully!")
            return redirect('employees')

    else:
        form = EmployeeForm()

    return render(request, 'admin/add_employee.html', {'form': form, 'title': 'Add New Employee'})


@user_passes_test(lambda user: user.is_superuser, login_url='login')
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    user = employee.user  # Get associated user before deleting employee
    employee.delete()
    user.delete()  # Delete associated user
    messages.success(request, "Employee deleted successfully!")
    return redirect('employees')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Employee, Profile
from .forms import EmployeeForm

@user_passes_test(lambda user: user.is_superuser, login_url='login')
def update_employee(request, employee_id):
    
    employee = get_object_or_404(Employee, pk=employee_id)
    user = employee.user  # Associated User object
    profile, created = Profile.objects.get_or_create(user=user)  # Ensure profile exists
    title = "Update Employee ("+ user.first_name +" "+ user.last_name + ")"

    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES, instance=employee)

        if form.is_valid():
            # Update User model
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            # Update Profile model
            profile.contact = form.cleaned_data['contact']
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']  # Save new profile image
            profile.save()

            # Update Employee model
            employee = form.save(commit=False)
            employee.user = user  # Ensure correct user assignment
            employee.save()

            messages.success(request, "Employee updated successfully!")
            return redirect('employees')  # Redirect to employee list page

        else:
            print("Form Errors:", form.errors)
            messages.error(request, "Please correct the errors below.")  # Show form errors


    else:
        # Pre-fill form with existing data
        form = EmployeeForm(instance=employee, initial={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'password': user.password,
            'contact': profile.contact,
        })

    return render(request, 'admin/add_employee.html', {'form': form, 'employee': employee, 'title': title})


@user_passes_test(lambda user: user.is_superuser, login_url='login')
def departments(request):
    departments = Department.objects.all()  # Fetch all departments
    return render(request, 'admin/departments.html', {'departments': departments})


from .forms import DepartmentForm

@user_passes_test(lambda user: user.is_superuser, login_url='login')
def add_department(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department added successfully!")
            return redirect('departments')  # Redirect to department list view after adding
    else:
        form = DepartmentForm()
    
    return render(request, 'admin/addDepartment.html', {'form': form})


def update_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)

    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully!")
            return redirect("departments")  # Change to your department list view
        else:
            messages.error(request, "Error updating department. Please check the form.")
    else:
        form = DepartmentForm(instance=department)

    return render(request, "admin/update_department.html", {"form": form, "department": department})

@user_passes_test(lambda user: user.is_superuser, login_url='login')
def delete_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    department.delete()
    messages.success(request, "Department deleted successfully!")
    return redirect("departments")  # Redirect to department list after deletion

import cv2
import face_recognition
import numpy as np
from django.contrib import messages
from django.shortcuts import render
from .models import Employee, Attendance
from django.utils.timezone import now

def recognize_employee(request):
    if request.method == "POST":
        # Open webcam
        video_capture = cv2.VideoCapture(0)
        ret, frame = video_capture.read()
        video_capture.release()

        if not ret:
            messages.error(request, "Failed to capture image from camera.")
            return render(request, 'attendance/face_recognition.html')

        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect face locations (top, right, bottom, left)
        face_locations = face_recognition.face_locations(rgb_frame, model='hog')

        if not face_locations:
            messages.error(request, "No face detected.")
            return render(request, 'attendance/face_recognition.html')

        # Now safely get encodings
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if not face_encodings:
            messages.error(request, "Face encoding failed.")
            return render(request, 'attendance/face_recognition.html')

        encoding = face_encodings[0]  # First face encoding

        # Load all employees and compare the encoding
        employees = Employee.objects.exclude(face_encoding=None)
        matched = False

        for emp in employees:
            stored_encoding = np.array(emp.get_face_encoding())  # Get the deserialized encoding

            # Calculate Euclidean distance between stored encoding and captured encoding
            distance = np.linalg.norm(stored_encoding - encoding)

            if distance < 0.6:  # Threshold for matching (can adjust if needed)
                # Mark attendance
                Attendance.objects.create(
                    emp=emp,
                    date=now().date(),
                    status="Present"
                )
                messages.success(request, f"Attendance marked for {emp.user.username}")
                matched = True
                break

        if not matched:
            messages.warning(request, "Face not recognized in the system.")

        return render(request, 'attendance/face_recognition.html')

    return render(request, 'attendance/face_recognition.html')

def attendance_list(request):
    # attendances = Attendance.objects.select_related('emp__user').order_by('-date')
    attendances = Attendance.objects.order_by('-date')
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})

