import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import now

from .models import Loan

logger = logging.getLogger(__name__)


@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject="Book Loaned Successfully",
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


@shared_task
def check_overdue_loans():
    overdue_loans = Loan.objects.filter(
        is_returned=False, due_date__lt=now().date(), remainder_sent=False
    )
    count = overdue_loans.count()
    loan_word = "loan" if count in [0, 1] else "loans"
    logger.info(f"Found {count} overdue {loan_word}")

    for loan in overdue_loans:
        user = loan.member.user

        send_mail(
            subject="Overdue Book Reminder",
            message=f'Dear {user.username},\n\ndo note that "{loan.book.title} is overdue".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        loan.remainder_sent = True
        loan.save()

        logger.info(f"Sent reminder for loan {loan.id} to {user.email}")
