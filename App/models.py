from django.db import models
from django.contrib.auth.models import User
import pickle


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Department(models.Model):
    dep_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dep = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[("Active", "Active"), ("Inactive", "Inactive")])

    # ➔ NEW FIELD to store face encoding
    face_encoding = models.BinaryField(blank=True, null=True)

    def set_face_encoding(self, encoding):
        self.face_encoding = pickle.dumps(encoding)

    def get_face_encoding(self):
        if self.face_encoding:
            return pickle.loads(self.face_encoding)
        return None

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.role}"


class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[("Present", "Present"), ("Absent", "Absent")])

    def __str__(self):
        return f"{self.emp.user.username} - {self.date} - {self.status}"


class Leaves(models.Model):
    leave_id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()

    def __str__(self):
        return f"Leave Request by {self.emp.user.username} from {self.start_date} to {self.end_date}"


class Apology(models.Model):
    apology_id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField()

    def __str__(self):
        return f"Apology by {self.emp.user.username} on {self.date}"


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"Report by {self.user.username} on {self.date}"


from django import forms
from django.contrib.auth.models import User
from .models import Employee, Department


from django import forms
from django.contrib.auth.models import User
from .models import Employee, Department, Profile
import face_recognition

class EmployeeForm(forms.ModelForm):
    # Fields for user registration
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # Fields for employee creation
    dep = forms.ModelChoiceField(queryset=Department.objects.all())
    role = forms.CharField(max_length=50)
    status = forms.ChoiceField(choices=[("Active", "Active"), ("Inactive", "Inactive")])
    contact = forms.CharField(max_length=15)
    profile_image = forms.ImageField(required=False)  # Optional profile image

    class Meta:
        model = Employee
        fields = ['dep', 'role', 'status', 'contact', 'profile_image']

    def save(self, commit=True):
        # Create the User instance
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )

        # Create the Employee instance and associate with the created User
        employee = super().save(commit=False)
        employee.user = user  # Associate with the created user

        # Save the employee instance if commit is True
        if commit:
            employee.save()

        # Create the Profile instance and associate it with the user
        profile = Profile.objects.create(
            user=user,
            profile_image=self.cleaned_data.get('profile_image'),  # Handle optional profile image
            contact=self.cleaned_data['contact']
        )

        # Capture face encoding if the profile image exists
        if self.cleaned_data.get('profile_image'):
            image_path = self.cleaned_data['profile_image'].path
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)[0]
            employee.set_face_encoding(encoding)
            employee.save()

        return employee