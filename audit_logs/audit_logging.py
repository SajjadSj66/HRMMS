from .models import *
from django.utils.timezone import now
import threading


def log_audit_trail(user, action, ip_address=None):
    """Logs user actions asynchronously to prevent blocking the main request."""

    def log():
        AuditLog.objects.create(user=user, action=action, ip_address=ip_address)

    threading.Thread(target=log).start()
