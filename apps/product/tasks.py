from apps.base.mail import send_mail
from celery import shared_task
from django.utils.timezone import now
from apps.product.models import TableBooking
import logging
from django.db.models import F
logger = logging.getLogger(__name__)

def booking_expired():
    """
    Function to mark expired table bookings as inactive.
    """
    expired_bookings = TableBooking.objects.filter(
        is_active=True,
        # start_time__lt=now() - F('duration') # <-<, duration in a minutes
        # when start time plus duration is greater than or equal now, then it is not expired
        start_time__lte=now() - F('duration') # or 
    )
    
    for booking in expired_bookings:
        booking.is_active = False
        booking.save()

        # Optionally, update the status of the associated FloorTable
        booking.floor_table.is_booked = False
        booking.floor_table.save()
    
    return expired_bookings.count()

@shared_task
def release_expired_bookings():
    """
    Task to mark expired table bookings as inactive.
    """
    count  =  booking_expired()
    print("\033[1;31mCelery task completed.\033[0m")
    return f"{count} bookings released."

@shared_task
def send_email(sub, body, to):
    print("Stated!")
    send_mail(sub, body, to)
    print("Complated!")