from celery import shared_task
from django.core.mail import send_mail
from .models import LabResult

@shared_task

def notify_patient_of_lab_result(lab_result_id):
    try:
        lab_result = LabResult.objects.get(id=lab_result_id)
        patient_email = lab_result.patient.email
        send_mail(
            "Your Lab Result is Ready",
            f"Dear {lab_result.patient.get_full_name()} , your lab test ({lab_result.test_name}) is now available",
            "<EMAIL>",
            [patient_email],
            fail_silently=True,
        )
    except LabResult.DoesNotExist:
        pass
