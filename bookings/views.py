from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import BookingForm
from .services.booking import find_available_table
from .models import Restaurant, Booking
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Count
from datetime import date
from .models import Restaurant, Booking, Table, OpeningHours
from .forms_owner import TableForm, OpeningHoursForm

# -------------------
# Booking Creation
# -------------------

class CreateBookingView(View):
    def get(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        form = BookingForm(initial={'restaurant': restaurant.id})
        return render(request, "bookings/create_booking.html", {
            "form": form,
            "restaurant": restaurant
        })

    def post(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        print("FORM SUBMITTED")
        print(request.POST)

        form = BookingForm(request.POST)

        if not form.is_valid():
           return render(request, "bookings/create_booking.html", {
            "form": form,
            "restaurant": restaurant
        })

        data = form.cleaned_data
        user = request.user if request.user.is_authenticated else None

        table, error = find_available_table(
            restaurant=restaurant,
            date=data['date'],
            time=data['time'],
             party_size=data['party_size'],
             user=user
        )

        if error:
            messages.error(request, error)
            return render(request, "bookings/create_booking.html", {
            "form": form,
            "restaurant": restaurant
             })

        booking = Booking.objects.create(
            user=user,
            restaurant=restaurant,
            table=table,
            date=data['date'],
            time=data['time'],
            party_size=data['party_size'],
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            notes=data['notes'],
        )

        return redirect("booking_success")

# -------------------
# Owner Dashboard
# -------------------

class OwnerDashboardView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "bookings/owner_dashboard.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return Booking.objects.filter(
            restaurant__owner=self.request.user
        ).order_by("date", "time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        owner_bookings = Booking.objects.filter(
            restaurant__owner=self.request.user
        )

        context["total_bookings"] = owner_bookings.count()

        context["today_bookings"] = owner_bookings.filter(
            date=date.today()
        ).count()

        context["upcoming_bookings"] = owner_bookings.filter(
            date__gte=date.today()
        ).count()

        return context
    
class OwnerTablesView(LoginRequiredMixin, ListView):
    model = Table
    template_name = "bookings/owner_tables.html"
    context_object_name = "tables"

    def get_queryset(self):
        return Table.objects.filter(
            restaurant__owner=self.request.user
        )
    



class AddTableView(LoginRequiredMixin, CreateView):
    model = Table
    form_class = TableForm
    template_name = "bookings/add_table.html"

    def form_valid(self, form):
        restaurant = Restaurant.objects.filter(owner=self.request.user).first()
        form.instance.restaurant = restaurant
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("owner_tables")
    

class EditTableView(LoginRequiredMixin, UpdateView):
    model = Table
    form_class = TableForm
    template_name = "bookings/edit_table.html"

    def get_success_url(self):
        return reverse_lazy("owner_tables")
    

class OwnerOpeningHoursView(LoginRequiredMixin, ListView):
    model = OpeningHours
    template_name = "bookings/owner_opening_hours.html"
    context_object_name = "hours"

    def get_queryset(self):
        return OpeningHours.objects.filter(
            restaurant__owner=self.request.user
        )

class AddOpeningHoursView(LoginRequiredMixin, CreateView):
    model = OpeningHours
    form_class = OpeningHoursForm
    template_name = "bookings/add_opening_hours.html"

    def form_valid(self, form):
        restaurant = Restaurant.objects.filter(owner=self.request.user).first()
        form.instance.restaurant = restaurant
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("owner_opening_hours")



@login_required
def owner_cancel_booking(request, pk):
    booking = get_object_or_404(
        Booking,
        pk=pk,
        restaurant__owner=request.user
    )
    booking.status = 'cancelled'
    booking.save()
    return redirect('owner_dashboard')


# -------------------
# Restaurant Views
# -------------------

class RestaurantListView(ListView):
    model = Restaurant
    template_name = "bookings/restaurant_list.html"
    context_object_name = "restaurants"


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = "bookings/restaurant_detail.html"
    context_object_name = "restaurant"


# -------------------
# User Reservations
# -------------------

@login_required
def my_reservations(request):
    bookings = Booking.objects.filter(
        user=request.user
    ).order_by('-date', '-time')

    return render(
        request,
        'bookings/my_reservations.html',
        {'bookings': bookings}
    )


# -------------------
# Home
# -------------------

def home(request):
    return render(request, 'home.html')


def booking_success(request):
    return render(request, 'bookings/booking_success.html')

def home(request):
    restaurants = Restaurant.objects.all()  # all restaurants
    top_picks = restaurants[:5]  # pick first 5 as top picks
    return render(request, 'home.html', {'top_picks': top_picks})