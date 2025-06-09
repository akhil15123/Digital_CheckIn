

# **Digital CheckIn System**

This is a **Digital CheckIn** system built with **Django** for managing employee records, attendance, leave requests, and employee profiles. It uses face recognition for automatic attendance marking and integrates with Django's authentication system.

## **Table of Contents**

* [Project Overview](#project-overview)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Installation](#installation)
* [Setup Instructions](#setup-instructions)
* [Folder Structure](#folder-structure)
* [Contributors](#contributors)
* [License](#license)

## **Project Overview**

The Digital CheckIn system is a complete solution for managing employee information, marking attendance, managing leave requests, and providing an easy-to-use interface for both admins and employees. Employees can register, update their profile, and their attendance is tracked using face recognition.

Admins have a dashboard that shows employee details, attendance records, and allows them to manage employees, departments, and leaves.

### **Main Features**

* **User Authentication**: Allows employee registration, login, and profile management.
* **Employee Management**: Admin can add, update, and delete employees.
* **Attendance Management**: Face recognition-based attendance marking.
* **Leave Requests**: Employees can submit leave requests, which are managed by the admin.
* **Department Management**: Admin can manage departments.
* **Admin Dashboard**: Admin has a dashboard that shows overall employee information, attendance statistics, and reports.
* **Profile Image**: Employees can upload and update their profile images.

## **Technologies Used**

* **Django**: Web framework used for backend development.
* **Python**: Programming language used for development.
* **SQLite**: Database for storing data (can be swapped with PostgreSQL or MySQL).
* **Face Recognition**: Used for employee attendance marking.
* **OpenCV**: Used for handling webcam interactions for face recognition.
* **Bootstrap**: Used for the front-end UI and styling.
* **HTML/CSS**: Front-end technologies for structuring and styling the web pages.

## **Features**

* **Registration**: Employees can register by providing their basic information such as username, first name, last name, email, password, contact number, profile image, and department.
* **Login**: Employees can log in to access their profiles, mark attendance, and request leaves.
* **Profile Management**: Employees can update their contact information and profile image.
* **Face Recognition Attendance**: Employees’ attendance is marked using face recognition when they log in.
* **Admin Panel**: Admin can manage employees, departments, attendance, and leave requests.
* **Leave Management**: Admin can approve or deny leave requests submitted by employees.
* **Department Management**: Admin can add, update, and delete departments.

## **Installation**

### **Step 1: Clone the Repository**

Clone the repository from GitHub:

```bash
[git clone https://github.com/your-username/digital-checkin.git](https://github.com/akhil15123/Digital_CheckIn.git)
```

### **Step 2: Install Python and Dependencies**

Ensure that you have **Python 3.10+** and **pip** installed.

1. Create a virtual environment:

   ```bash
   python3 -m venv digital-checkin-env
   ```

2. Activate the virtual environment:

   **On Mac/Linux:**

   ```bash
   source digital-checkin-env/bin/activate
   ```

   **On Windows:**

   ```bash
   .\digital-checkin-env\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### **Step 3: Set Up the Database**

1. Run migrations to set up the database:

   ```bash
   python manage.py migrate
   ```

2. Create a superuser for accessing the Django admin panel:

   ```bash
   python manage.py createsuperuser
   ```

### **Step 4: Run the Development Server**

Start the Django development server:

```bash
python manage.py runserver
```

You can now access the application at `http://127.0.0.1:8000`.

## **Setup Instructions**

1. **Face Recognition Setup:**

   * The face recognition system uses **OpenCV** and **dlib** libraries. Make sure you have the required libraries installed:

     * `opencv-python`
     * `dlib`
     * `face_recognition`

   * The system captures employee photos for face encoding during employee registration. Ensure that you have a webcam to capture the face for attendance.

2. **Static Files**:

   * Make sure you run the following command to collect static files if you're deploying to production:

     ```bash
     python manage.py collectstatic
     ```

3. **Admin Access**:

   * Log in to the admin panel by going to `http://127.0.0.1:8000/admin` and using the superuser credentials you created during setup.
   * The admin panel allows you to manage employees, attendance, leaves, and departments.

## **Folder Structure**

Here’s a high-level overview of the folder structure:

```
digital-checkin/
├── account/                      # User authentication and profile management
│   ├── migrations/
│   ├── models.py                 # User and Profile models
│   ├── forms.py                  # User registration and profile forms
│   ├── views.py                  # Authentication, registration, and profile views
│   ├── urls.py                   # URLs for login, register, profile
│   └── templates/                # HTML templates
│       └── account/
│           ├── login.html
│           ├── register.html
│           └── profile.html
├── attendance/                   # Attendance and face recognition functionality
│   ├── models.py                 # Attendance and leave models
│   ├── views.py                  # Attendance handling and face recognition views
│   ├── templates/
│   │   └── attendance/
│   │       └── face_recognition.html
├── department/                   # Department management functionality
│   ├── models.py                 # Department models
│   ├── views.py                  # Department views
│   ├── forms.py                  # Department forms
│   └── templates/                # Department templates
├── manage.py                     # Django management script
└── requirements.txt              # Python dependencies
```

## **Contributors**

* **Akhil Bonthinayanivari** – Initial development and design.

Feel free to contribute to this project by forking it and submitting pull requests.

## **License**

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

### **Final Notes**

