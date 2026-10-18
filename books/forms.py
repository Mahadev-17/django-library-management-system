from django import forms
from django.db.models import F
from .models import Book, Student, BookIssue


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "isbn", "category", "quantity"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "author": forms.TextInput(attrs={"class": "form-control"}),
            "isbn": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "roll_no", "email", "phone", "course"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "roll_no": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "course": forms.TextInput(attrs={"class": "form-control"}),
        }


class BookIssueForm(forms.ModelForm):
    class Meta:
        model = BookIssue
        fields = ["book", "student", "due_date"]
        widgets = {
            "book": forms.Select(attrs={"class": "form-select"}),
            "student": forms.Select(attrs={"class": "form-select"}),
            "due_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["book"].queryset = Book.objects.filter(available__gt=0)
        self.fields["student"].queryset = Student.objects.all()
