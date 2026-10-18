from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import BookForm, StudentForm, BookIssueForm
from .models import Book, Student, BookIssue


@login_required
def dashboard(request):
    context = {
        "book_count": Book.objects.count(),
        "student_count": Student.objects.count(),
        "issued_count": BookIssue.objects.filter(returned=False).count(),
        "overdue_count": BookIssue.objects.filter(
            returned=False, due_date__lt=timezone.localdate()
        ).count(),
        "recent_issues": BookIssue.objects.select_related("book", "student")[:8],
        "today": timezone.localdate(),
    }
    return render(request, "books/dashboard.html", context)


@login_required
def book_list(request):
    query = request.GET.get("q", "").strip()
    books = Book.objects.all()
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query) |
            Q(category__icontains=query)
        )
    return render(request, "books/book_list.html", {"books": books, "query": query})


@login_required
def book_create(request):
    form = BookForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        book = form.save(commit=False)
        book.available = book.quantity
        book.save()
        messages.success(request, "Book added successfully.")
        return redirect("book_list")
    return render(request, "books/book_form.html", {"form": form, "page_title": "Add Book"})


@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if request.method == "POST" and form.is_valid():
        new_quantity = form.cleaned_data["quantity"]
        currently_issued = book.quantity - book.available
        if new_quantity < currently_issued:
            form.add_error("quantity", f"Quantity cannot be below {currently_issued} currently issued book(s).")
        else:
            book = form.save(commit=False)
            book.available = new_quantity - currently_issued
            book.save()
            messages.success(request, "Book updated successfully.")
            return redirect("book_list")
    return render(request, "books/book_form.html", {"form": form, "page_title": "Edit Book"})


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        try:
            book.delete()
            messages.success(request, "Book deleted successfully.")
        except Exception:
            messages.error(request, "This book has issue records and cannot be deleted.")
        return redirect("book_list")
    return render(request, "books/confirm_delete.html", {"object": book, "object_type": "book"})


@login_required
def student_list(request):
    query = request.GET.get("q", "").strip()
    students = Student.objects.all()
    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(student_id__icontains=query) |
            Q(email__icontains=query) |
            Q(course__icontains=query)
        )
    return render(request, "books/student_list.html", {"students": students, "query": query})


@login_required
def student_create(request):
    form = StudentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Student added successfully.")
        return redirect("student_list")
    return render(request, "books/student_form.html", {"form": form, "page_title": "Add Student"})


@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Student updated successfully.")
        return redirect("student_list")
    return render(request, "books/student_form.html", {"form": form, "page_title": "Edit Student"})


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        try:
            student.delete()
            messages.success(request, "Student deleted successfully.")
        except Exception:
            messages.error(request, "This student has issue records and cannot be deleted.")
        return redirect("student_list")
    return render(request, "books/confirm_delete.html", {"object": student, "object_type": "student"})


@login_required
def issue_list(request):
    query = request.GET.get("q", "").strip()
    issues = BookIssue.objects.select_related("book", "student")
    if query:
        issues = issues.filter(
            Q(book__title__icontains=query) |
            Q(student__name__icontains=query) |
            Q(student__student_id__icontains=query)
        )
    return render(request, "books/issue_list.html", {"issues": issues, "query": query, "today": timezone.localdate()})


@login_required
@transaction.atomic
def issue_create(request):
    form = BookIssueForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        book = Book.objects.select_for_update().get(pk=form.cleaned_data["book"].pk)
        if book.available < 1:
            form.add_error("book", "No copies of this book are currently available.")
        else:
            issue = form.save(commit=False)
            issue.book = book
            issue.issue_date = timezone.localdate()
            issue.save()
            book.available -= 1
            book.save(update_fields=["available"])
            messages.success(request, "Book issued successfully.")
            return redirect("issue_list")
    return render(request, "books/issue_form.html", {"form": form, "page_title": "Issue Book"})


@login_required
@transaction.atomic
def issue_return(request, pk):
    issue = get_object_or_404(
        BookIssue.objects.select_related("book"), pk=pk, returned=False
    )
    if request.method == "POST":
        issue.returned = True
        issue.return_date = timezone.localdate()
        issue.save(update_fields=["returned", "return_date"])
        issue.book.available += 1
        issue.book.save(update_fields=["available"])
        if issue.fine:
            messages.warning(request, f"Book returned. Late fine: ₹{issue.fine}")
        else:
            messages.success(request, "Book returned successfully.")
    return redirect("issue_list")
