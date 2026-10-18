from django.contrib import admin
from .models import Book, Student, Teacher, BookIssue


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "isbn", "category", "quantity", "available")
    search_fields = ("title", "author", "isbn", "category")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("roll_no", "name", "email", "phone", "course")
    search_fields = ("roll_no", "name", "email")


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("teacher_id", "name", "department", "email", "phone")
    search_fields = ("teacher_id", "name", "department")


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "student",
        "teacher",
        "issue_date",
        "due_date",
        "returned",
        "return_date",
    )
    list_filter = ("returned", "issue_date", "due_date")
    search_fields = (
        "book__title",
        "student__name",
        "student__roll_no",
        "teacher__name",
        "teacher__teacher_id",
    )
