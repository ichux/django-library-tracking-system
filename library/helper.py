from datetime import timedelta

from django.conf import settings
from django.utils import timezone


def due_on():
    return timezone.now().date() + timedelta(days=settings.DEFAULT_LOAN_PERIOD_DAYS)
