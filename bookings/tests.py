from django.test import TestCase
from django.contrib.auth.models import User
from bookings.models import Booking, Restaurant
from django.core.exceptions import ValidationError
class BookingTestCase(TestCase):

   def test_invalid_booking(self):
    booking = Booking(
        
        party_size=10
    )

    with self.assertRaises(ValidationError):
        booking.full_clean()