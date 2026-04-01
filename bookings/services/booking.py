from datetime import timedelta
from django.db.models import Q
from datetime import datetime, time, date
from bookings.models import Booking, Table, OpeningHours

RESERVATION_DURATION = 90  # minutes

def find_available_table(restaurant, date, time, party_size, user=None):
    # 1. Prevent customer double-booking same restaurant/time
    if user:
        existing = Booking.objects.filter(
            user=user,
            restaurant=restaurant,
            date=date,
            time=time,
            status="confirmed"
        ).exists()
        if existing:
            return None, "You already have a booking at this restaurant for that time."

    # 2. Check restaurant opening hours
    weekday = date.weekday()
    try:
        hours = OpeningHours.objects.get(restaurant=restaurant, day_of_week=weekday)
    except OpeningHours.DoesNotExist:
        return None, "Restaurant is closed on this day."

    if not (hours.open_time <= time <= hours.close_time):
        return None, "Selected time is outside restaurant opening hours."

    # 3. Find candidate tables (best-fit = smallest table >= party_size)
    candidate_tables = Table.objects.filter(restaurant=restaurant, capacity__gte=party_size).order_by('capacity')

    if not candidate_tables.exists():
        return None, "No table can accommodate that party size."

    # Prepare time window for overlap check
    start_dt = datetime.combine(date, time)
    end_dt = start_dt + timedelta(minutes=RESERVATION_DURATION)

    for table in candidate_tables:
        overlapping = Booking.objects.filter(
            table=table,
            status="confirmed",
            date=date
        ).filter(
            Q(time__lt=end_dt.time()) & Q(time__gte=start_dt.time())
        ).exists()

        if not overlapping:
            return table, None  # success

    return None, "No available tables at that time."
