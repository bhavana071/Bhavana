from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import *
from .forms import IssueBookForm

def index(request):
    return render(request, "index.html")

@login_required(login_url='/admin_login')
def add_book(request):
    if request.method == "POST":
        name = request.POST.get('name')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        category = request.POST.get('category')

        if name and author and isbn and category:
            Book.objects.create(name=name, author=author, isbn=isbn, category=category)
            return render(request, "add_book.html", {'alert': True})
    
    return render(request, "add_book.html")

@login_required(login_url='/admin_login')
def view_books(request):
    books = Book.objects.all()
    return render(request, "view_books.html", {'books': books})

@login_required(login_url='/admin_login')
def view_students(request):
    students = Student.objects.all()
    return render(request, "view_students.html", {'students': students})

@login_required(login_url='/admin_login')
def issue_book(request):
    form = IssueBookForm()
    if request.method == "POST":
        form = IssueBookForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return render(request, "issue_book.html", {'obj': obj, 'alert': True})

    return render(request, "issue_book.html", {'form': form})

@login_required(login_url='/admin_login')
def view_issued_book(request):
    issued_books = IssuedBook.objects.select_related('student', 'book').all()
    details = []

    for issued_book in issued_books:
        days_overdue = (date.today() - issued_book.issued_date).days
        fine = max(0, (days_overdue - 14) * 5)

        details.append((
            issued_book.student.user,
            issued_book.student.user_id,
            issued_book.book.name,
            issued_book.book.isbn,
            issued_book.issued_date,
            issued_book.expiry_date,
            fine
        ))

    return render(request, "view_issued_book.html", {'issuedBooks': issued_books, 'details': details})

@login_required(login_url='/student_login')
def student_issued_books(request):
    student = Student.objects.filter(user=request.user).first()
    if not student:
        return HttpResponse("Student not found.")

    issued_books = IssuedBook.objects.filter(student=student)
    li1, li2 = [], []

    for issued_book in issued_books:
        li1.append((
            request.user.id,
            request.user.get_full_name(),
            issued_book.book.name,
            issued_book.book.author
        ))

        days_overdue = (date.today() - issued_book.issued_date).days
        fine = max(0, (days_overdue - 14) * 5)

        li2.append((
            issued_book.issued_date,
            issued_book.expiry_date,
            fine
        ))

    return render(request, "student_issued_books.html", {'li1': li1, 'li2': li2})

@login_required(login_url='/student_login')
def profile(request):
    return render(request, "profile.html")

@login_required(login_url='/student_login')
def edit_profile(request):
    student = Student.objects.get(user=request.user)
    if request.method == "POST":
        student.user.email = request.POST.get('email', student.user.email)
        student.phone = request.POST.get('phone', student.phone)
        student.branch = request.POST.get('branch', student.branch)
        student.classroom = request.POST.get('classroom', student.classroom)
        student.roll_no = request.POST.get('roll_no', student.roll_no)

        student.user.save()
        student.save()
        return render(request, "edit_profile.html", {'alert': True})

    return render(request, "edit_profile.html")

@login_required(login_url='/admin_login')
def delete_book(request, myid):
    Book.objects.filter(id=myid).delete()
    return redirect("/view_books")

@login_required(login_url='/admin_login')
def delete_student(request, myid):
    Student.objects.filter(id=myid).delete()
    return redirect("/view_students")

@login_required(login_url='/student_login')
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        
        user = request.user
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            return render(request, "change_password.html", {'alert': True})
        else:
            return render(request, "change_password.html", {'currpasswrong': True})

    return render(request, "change_password.html")

def student_registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        branch = request.POST.get('branch')
        classroom = request.POST.get('classroom')
        roll_no = request.POST.get('roll_no')
        image = request.FILES.get('image')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, "student_registration.html", {'passnotmatch': True})

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        Student.objects.create(user=user, phone=phone, branch=branch, classroom=classroom, roll_no=roll_no, image=image)

        return render(request, "student_registration.html", {'alert': True})

    return render(request, "student_registration.html")

def student_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect("/profile") if not user.is_superuser else HttpResponse("You are not a student!!")

        return render(request, "student_login.html", {'alert': True})

    return render(request, "student_login.html")

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect("/add_book") if user.is_superuser else HttpResponse("You are not an admin.")

        return render(request, "admin_login.html", {'alert': True})

    return render(request, "admin_login.html")

def Logout(request):
    logout(request)
    return redirect("/")
