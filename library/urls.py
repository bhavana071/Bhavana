from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    # Book Management
    path("add_book/", views.add_book, name="add_book"),
    path("view_books/", views.view_books, name="view_books"),
    path("delete_book/<int:myid>/", views.delete_book, name="delete_book"),

    # Student Management
    path("view_students/", views.view_students, name="view_students"),
    path("delete_student/<int:myid>/", views.delete_student, name="delete_student"),
    
    # Book Issuing & Viewing
    path("issue_book/", views.issue_book, name="issue_book"),
    path("view_issued_book/", views.view_issued_book, name="view_issued_book"),
    path("student_issued_books/", views.student_issued_books, name="student_issued_books"),

    # Student Profile
    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),

    # Authentication & Registration
    path("student_registration/", views.student_registration, name="student_registration"),
    path("student_login/", views.student_login, name="student_login"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("change_password/", views.change_password, name="change_password"),
    path("logout/", views.Logout, name="logout"),
]
