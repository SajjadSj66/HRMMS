from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from users.models import User
from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer
from datetime import timedelta

class AppointmentSerializerTest(TestCase):

    def setUp(self):
        """Create test users (patient, doctor, and nurse)."""
        self.patient = User.objects.create_user(username="patient1", password="password1", role="patient")
        self.doctor = User.objects.create_user(username="doctor1", password="password2", role="doctor")
        self.nurse = User.objects.create_user(username="nurse1", password="password3", role="nurse")

        # Test data for a valid appointment
        self.valid_data = {
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'nurse_id': self.nurse.id,
            'appointment_datetime': timezone.now() + timedelta(days=1),
            'status': 'Scheduled',
            'reason': 'Routine Checkup',
            'notes': 'Patient is healthy'
        }

    def test_create_appointment_valid_data(self):
        """Test creating an appointment with valid data."""
        serializer = AppointmentSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        appointment = serializer.save()

        self.assertEqual(appointment.patient, self.patient)
        self.assertEqual(appointment.doctor, self.doctor)
        self.assertEqual(appointment.nurse, self.nurse)
        self.assertEqual(appointment.status, 'Scheduled')
        self.assertEqual(appointment.reason, 'Routine Checkup')

    def test_create_appointment_in_the_past(self):
        """Test creating an appointment with a datetime in the past."""
        data = self.valid_data.copy()
        data['appointment_datetime'] = timezone.now() - timedelta(days=1)

        serializer = AppointmentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('appointment_datetime', serializer.errors)
        self.assertEqual(str(serializer.errors['appointment_datetime'][0]), 'The appointment is in the past')

    def test_create_appointment_without_login(self):
        """Test creating an appointment without being logged in."""
        data = self.valid_data.copy()

        # Mock an unauthenticated request
        request = None  # Simulating no request or unauthenticated user
        serializer = AppointmentSerializer(data=data, context={'request': request})

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_create_appointment_invalid_user_roles(self):
        """Test creating an appointment with invalid user roles (non-patient or non-doctor)."""
        invalid_patient = User.objects.create_user(username="invalid_patient", password="password4", role="doctor")
        invalid_doctor = User.objects.create_user(username="invalid_doctor", password="password5", role="nurse")
        invalid_nurse = User.objects.create_user(username="invalid_nurse", password="password6", role="patient")

        data = self.valid_data.copy()
        data['patient_id'] = invalid_patient.id
        data['doctor_id'] = invalid_doctor.id
        data['nurse_id'] = invalid_nurse.id

        serializer = AppointmentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('patient_id', serializer.errors)
        self.assertIn('doctor_id', serializer.errors)
        self.assertIn('nurse_id', serializer.errors)

    def test_create_appointment_missing_field(self):
        """Test creating an appointment with missing required fields."""
        data = self.valid_data.copy()
        del data['reason']  # Remove required field

        serializer = AppointmentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('reason', serializer.errors)

    def test_create_appointment_with_invalid_status(self):
        """Test creating an appointment with an invalid status."""
        data = self.valid_data.copy()
        data['status'] = 'InvalidStatus'  # Invalid status

        serializer = AppointmentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('status', serializer.errors)
        self.assertEqual(str(serializer.errors['status'][0]), '“InvalidStatus” is not a valid choice.')

    def test_filter_appointments_by_date(self):
        """Test filtering appointments by date logic in serializer."""
        # Create appointments with different times
        future_appointment = Appointment.objects.create(**self.valid_data)
        past_appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            nurse=self.nurse,
            appointment_datetime=timezone.now() - timedelta(days=2),
            status="Scheduled",
            reason="Follow-up",
            notes="Patient has no issues."
        )

        # Verify the appointments
        appointments = Appointment.objects.all()
        self.assertEqual(len(appointments), 2)
        self.assertIn(future_appointment, appointments)
        self.assertIn(past_appointment, appointments)
