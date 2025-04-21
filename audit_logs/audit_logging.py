import threading
import logging
from .models import AuditLog

logger = logging.getLogger(__name__)

def log_audit_trail(user, action, ip_address=None):
    """Logs user actions asynchronously to prevent blocking the main request."""

    if not user or not action:
        logger.warning("Audit log skipped: Missing user or action.")
        return

    def log():
        try:
            AuditLog.objects.create(user=user, action=action, ip_address=ip_address)
        except Exception as e:
            logger.error(f"Failed to create audit log: {e}")

    threading.Thread(target=log).start()