from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_booking_confirmation(booking):
    subject = f"Reservation Confirmed at {booking.restaurant.name}"
    from_email = "no-reply@reservations.com"
    to = [booking.email]

    html_content = render_to_string("emails/booking_confirmation.html", {
        "booking": booking
    })

    msg = EmailMultiAlternatives(subject, "", from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
