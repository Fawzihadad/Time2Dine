from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator



class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.name

class OpeningHours(models.Model):
    DAYS = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAYS)
    open_time = models.TimeField()
    close_time = models.TimeField()

    def __str__(self):
        return f"{self.restaurant.name} - {self.get_day_of_week_display()}"

class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=50)  # e.g. T1, Booth 3
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.restaurant.name} - {self.identifier} ({self.capacity})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ("confirmed", "Confirmed"),
        ("canceled", "Canceled"),
    ]

    user = models.ForeignKey(
    User,
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
)

    restaurant = models.ForeignKey(
    Restaurant,
    on_delete=models.CASCADE
)

    table = models.ForeignKey(
    Table,
    null=True,
    blank=True,
    on_delete=models.SET_NULL
)


    date = models.DateField()
    time = models.TimeField()
    duration_minutes = models.IntegerField(default=90)  # fixed duration

    party_size = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="confirmed")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name} - {self.date} {self.time}"
