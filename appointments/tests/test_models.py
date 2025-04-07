from django.test import TestCase
from users.models import User
from appointments.models import Appointment
from datetime import datetime, timedelta


class AppointmentModelTest(TestCase):

    def setUp(self):
        """Create test users (patient, doctor, and nurse)."""
        self.patient = User.objects.create_user(username="patient1", password="password1", is_staff=False)
        self.doctor = User.objects.create_user(username="doctor1", password="password2", is_staff=True)
        self.nurse = User.objects.create_user(username="nurse1", password="password3", is_staff=False)

        # Create an appointment for patient with doctor
        self.appointment_data = {
            "patient": self.patient,
            "doctor": self.doctor,
            "nurse": self.nurse,
            "appointment_datetime": datetime.now() + timedelta(days=1),
            "status": "Scheduled",
            "reason": "Routine Checkup",
            "notes": "Patient has no known allergies."
        }

    def test_create_appointment(self):
        """Test creating an appointment successfully."""
        appointment = Appointment.objects.create(**self.appointment_data)
        self.assertEqual(appointment.patient, self.patient)
        self.assertEqual(appointment.doctor, self.doctor)
        self.assertEqual(appointment.status, "Scheduled")
        self.assertEqual(appointment.reason, "Routine Checkup")
        self.assertIsNotNone(appointment.appointment_datetime)
        self.assertEqual(str(appointment),
                         f"Appointment: {self.patient.username} with {self.doctor.username} on {appointment.appointment_datetime} ({appointment.status})")

    def test_update_appointment(self):
        """Test updating an appointment's status and details."""
        appointment = Appointment.objects.create(**self.appointment_data)
        # Update appointment status
        appointment.status = "Completed"
        appointment.reason = "Routine Checkup - Follow-up"
        appointment.save()

        updated_appointment = Appointment.objects.get(id=appointment.id)
        self.assertEqual(updated_appointment.status, "Completed")
        self.assertEqual(updated_appointment.reason, "Routine Checkup - Follow-up")

    def test_cancel_appointment(self):
        """Test cancelling an appointment."""
        appointment = Appointment.objects.create(**self.appointment_data)
        appointment.status = "Cancelled"
        appointment.save()

        cancelled_appointment = Appointment.objects.get(id=appointment.id)
        self.assertEqual(cancelled_appointment.status, "Cancelled")

    def test_filter_appointments_by_date(self):
        """Test filtering appointments by date."""
        future_appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            nurse=self.nurse,
            appointment_datetime=datetime.now() + timedelta(days=2),
            status="Scheduled",
            reason="Routine Checkup"
        )
        past_appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            nurse=self.nurse,
            appointment_datetime=datetime.now() - timedelta(days=2),
            status="Scheduled",
            reason="Follow-up"
        )
        appointments_on_future_date = Appointment.objects.filter(
            appointment_datetime__date=datetime.now().date() + timedelta(days=2))
        self.assertEqual(appointments_on_future_date.count(), 1)
        self.assertEqual(appointments_on_future_date[0], future_appointment)

    def test_filter_appointments_by_status(self):
        """Test filtering appointments by status."""
        scheduled_appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            nurse=self.nurse,
            appointment_datetime=datetime.now() + timedelta(days=1),
            status="Scheduled",
            reason="Routine Checkup"
        )
        completed_appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            nurse=self.nurse,
            appointment_datetime=datetime.now() + timedelta(days=2),
            status="Completed",
            reason="Follow-up"
        )
        cancelled_appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            nurse=self.nurse,
            appointment_datetime=datetime.now() + timedelta(days=3),
            status="Cancelled",
            reason="No Show"
        )

        scheduled_appointments = Appointment.objects.filter(status="Scheduled")
        self.assertEqual(scheduled_appointments.count(), 1)
        self.assertEqual(scheduled_appointments[0], scheduled_appointment)

        completed_appointments = Appointment.objects.filter(status="Completed")
        self.assertEqual(completed_appointments.count(), 1)
        self.assertEqual(completed_appointments[0], completed_appointment)

        cancelled_appointments = Appointment.objects.filter(status="Cancelled")
        self.assertEqual(cancelled_appointments.count(), 1)
        self.assertEqual(cancelled_appointments[0], cancelled_appointment)
