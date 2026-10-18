
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    isbn = models.CharField(max_length=20, blank=True)
    category = models.CharField(max_length=100, blank=True)

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(0)]
    )
    available = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} — {self.author}"


class Student(models.Model):
    roll_no = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    course = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.roll_no})"


class Teacher(models.Model):
    teacher_id = models.CharField(
        max_length=20,
        primary_key=True
    )
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.teacher_id})"


class BookIssue(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT,
        related_name="issues"
    )

    student = models.ForeignKey(
        Student,
        to_field="roll_no",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="issues"
    )

    teacher = models.ForeignKey(
        Teacher,
        to_field="teacher_id",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="issues"
    )

    issue_date = models.DateField(
        default=timezone.localdate
    )
    due_date = models.DateField()
    returned = models.BooleanField(default=False)
    return_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["returned", "due_date"]

    def clean(self):
        if bool(self.student_id) == bool(self.teacher_id):
            raise ValidationError(
                "Select either one student or one teacher."
            )

        if self.due_date and self.issue_date:
            if self.due_date < self.issue_date:
                raise ValidationError(
                    "Due date cannot be before issue date."
                )

    def __str__(self):
        borrower = self.student or self.teacher
        return f"{self.book.title} → {borrower}"

    @property
    def overdue_days(self):
        end_date = self.return_date or timezone.localdate()
        return max((end_date - self.due_date).days, 0)

    @property
    def fine(self):
        if self.returned:
            return self.overdue_days * 5
        return self.overdue_days * 5
