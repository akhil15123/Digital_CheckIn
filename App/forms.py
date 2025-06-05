from django import forms
from django.contrib.auth.models import User
from .models import Department, Profile, Employee

# 1️⃣ User Registration Form (purely for Register page)
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
        }


# 2️⃣ Profile Update Form (only profile image + contact info)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'contact']

        widgets = {
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
        }


# 3️⃣ Department Form (fully styled already)
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Department Name'}),
        }


# 4️⃣ Employee Form (this is the main form for Add/Update Employee)
class EmployeeForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
        required=False    # 👉 For update form password can be optional
    )
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
    )
    contact = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
    )
    dep = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    role = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter role'}),
    )
    status = forms.ChoiceField(
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Employee
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password',
            'profile_image', 'contact', 'dep', 'role', 'status'
        ]
