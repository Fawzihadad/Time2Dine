from django.urls import path
from django.views.generic import TemplateView
from .views import (
    home,
    CreateBookingView,
    OwnerDashboardView,
    owner_cancel_booking,
    RestaurantListView,
    RestaurantDetailView,
    my_reservations,
    booking_success,
    OwnerTablesView,
    AddTableView,
    EditTableView,
    OwnerOpeningHoursView,
    AddOpeningHoursView,
)

urlpatterns = [
    # Home
    path('', home, name='home'),
    
   
    # Restaurants
    path('restaurants/', RestaurantListView.as_view(), name='restaurant_list'),
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant_detail'),

    # Booking
    path('restaurants/<int:restaurant_id>/book/', CreateBookingView.as_view(), name='create_booking'),
    path('my-reservations/', my_reservations, name='my_reservations'),
    path('booking-success/', TemplateView.as_view(
    template_name="bookings/booking_success.html"
    ), name='booking_success'),
    # Owner
    path('owner/dashboard/', OwnerDashboardView.as_view(), name='owner_dashboard'),
    path('owner/cancel/<int:pk>/', owner_cancel_booking, name='owner_cancel_booking'),
    path('owner/tables/', OwnerTablesView.as_view(), name='owner_tables'),
    path('owner/tables/add/', AddTableView.as_view(), name='add_table'),
    path('owner/tables/edit/<int:pk>/', EditTableView.as_view(), name='edit_table'),

    path('owner/opening-hours/', OwnerOpeningHoursView.as_view(), name='owner_opening_hours'),
    path('owner/opening-hours/add/', AddOpeningHoursView.as_view(), name='add_opening_hours'),
]

