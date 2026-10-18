from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("books/", views.book_list, name="book_list"),
    path("books/add/", views.book_create, name="book_create"),
    path("books/<int:pk>/edit/", views.book_update, name="book_update"),
    path("books/<int:pk>/delete/", views.book_delete, name="book_delete"),
    path("students/", views.student_list, name="student_list"),
    path("students/add/", views.student_create, name="student_create"),
    path("students/<int:pk>/edit/", views.student_update, name="student_update"),
    path("students/<int:pk>/delete/", views.student_delete, name="student_delete"),
    path("issues/", views.issue_list, name="issue_list"),
    path("issues/add/", views.issue_create, name="issue_create"),
    path("issues/<int:pk>/return/", views.issue_return, name="issue_return"),
]
