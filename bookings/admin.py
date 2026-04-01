from django.contrib import admin
from .models import (
    Restaurant,
    Table,
    Booking,
    OpeningHours,
)

admin.site.register(Restaurant)
admin.site.register(Table)
admin.site.register(Booking)
admin.site.register(OpeningHours)

