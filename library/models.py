from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date

# Function to set expiry date 14 days from the issue date
def expiry():
    return date.today() + timedelta(days=14)

# Book model to store book details
class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)  # ISBN as a string (with or without dashes)
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} [{self.isbn}]"

# Student model to store student details
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=10)
    branch = models.CharField(max_length=10)
    roll_no = models.CharField(max_length=10, blank=True)  # You can make roll_no optional
    phone = models.CharField(max_length=10, blank=True)   # Optionally make phone field blank
    image = models.ImageField(upload_to="students/", blank=True)  # Set upload path for student images

    def __str__(self):
        return f"{self.user} [{self.branch}] [{self.classroom}] [{self.roll_no}]"

# IssuedBook model to store issued book details with foreign keys for student and book
class IssuedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # ForeignKey to Student model
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # ForeignKey to Book model
    issued_date = models.DateField(auto_now_add=True)  # Set the issue date automatically when created
    expiry_date = models.DateField(default=expiry)  # Set the expiry date to 14 days from issue date

    def __str__(self):
        return f"{self.book.name} issued to {self.student.user.username} until {self.expiry_date}"
