from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from appointments.models import Appointment
from datetime import timedelta
from django.utils import timezone


class AppointmentViewTest(TestCase):
    def setUp(self):
        """Create test users (patient, doctor, nurse) and appointment data."""
        self.client = APIClient()

        # Create users
        self.patient = User.objects.create_user(username="patient1", password="password1", role="patient")
        self.doctor = User.objects.create_user(username="doctor1", password="password2", role="doctor")
        self.nurse = User.objects.create_user(username="nurse1", password="password3", role="nurse")

        # Create an appointment
        self.appointment_data = {
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'nurse_id': self.nurse.id,
            'appointment_datetime': timezone.now() + timedelta(days=1),
            'status': 'Scheduled',
            'reason': 'Routine Checkup',
            'notes': 'Patient is healthy'
        }

        # Make an appointment as a patient
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            nurse=self.nurse,
            appointment_datetime=timezone.now() + timedelta(days=1),
            status="Scheduled",
            reason="Routine Checkup",
            notes="Patient is healthy"
        )

    def test_create_appointment_as_patient(self):
        """Test creating an appointment as a patient."""
        self.client.force_authenticate(user=self.patient)
        response = self.client.post('/appointments/', self.appointment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 2)  # One existing and the new one

    def test_create_appointment_as_non_patient(self):
        """Test creating an appointment as a non-patient (doctor, nurse)."""
        self.client.force_authenticate(user=self.doctor)
        response = self.client.post('/appointments/', self.appointment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.nurse)
        response = self.client.post('/appointments/', self.appointment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_appointment_as_doctor(self):
        """Test updating an appointment as a doctor."""
        self.client.force_authenticate(user=self.doctor)
        updated_data = {"status": "Completed", "notes": "Appointment completed successfully."}
        response = self.client.put(f'/appointments/{self.appointment.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, "Completed")
        self.assertEqual(self.appointment.notes, "Appointment completed successfully.")

    def test_update_appointment_as_nurse(self):
        """Test updating an appointment as a nurse."""
        self.client.force_authenticate(user=self.nurse)
        updated_data = {"status": "Completed", "notes": "Nurse assisted in the appointment."}
        response = self.client.put(f'/appointments/{self.appointment.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, "Completed")
        self.assertEqual(self.appointment.notes, "Nurse assisted in the appointment.")

    def test_update_appointment_as_non_doctor_nurse(self):
        """Test updating an appointment as a user who is neither doctor nor nurse."""
        self.client.force_authenticate(user=self.patient)
        updated_data = {"status": "Completed", "notes": "Patient marked appointment as completed."}
        response = self.client.put(f'/appointments/{self.appointment.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_appointment_as_patient(self):
        """Test deleting an appointment as a patient."""
        self.client.force_authenticate(user=self.patient)
        response = self.client.delete(f'/appointments/{self.appointment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 0)

    def test_delete_appointment_as_doctor(self):
        """Test deleting an appointment as a doctor."""
        self.client.force_authenticate(user=self.doctor)
        response = self.client.delete(f'/appointments/{self.appointment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 0)

    def test_delete_appointment_as_nurse(self):
        """Test deleting an appointment as a nurse."""
        self.client.force_authenticate(user=self.nurse)
        response = self.client.delete(f'/appointments/{self.appointment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 0)

    def test_delete_appointment_as_non_doctor_patient(self):
        """Test deleting an appointment as a user who is neither doctor nor patient."""
        self.client.force_authenticate(user=self.nurse)
        response = self.client.delete(f'/appointments/{self.appointment.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_appointments_by_role(self):
        """Test filtering appointments by user role."""
        # Get patient appointments
        self.client.force_authenticate(user=self.patient)
        response = self.client.get('/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only the patient's appointment

        # Get doctor appointments
        self.client.force_authenticate(user=self.doctor)
        response = self.client.get('/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only the doctor's appointment

        # Get nurse appointments
        self.client.force_authenticate(user=self.nurse)
        response = self.client.get('/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only the nurse's appointment

    def test_filter_appointments_by_status(self):
        """Test filtering appointments by status."""
        completed_appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            nurse=self.nurse,
            appointment_datetime=timezone.now() + timedelta(days=2),
            status="Completed",
            reason="Routine Checkup",
            notes="Patient is healthy"
        )

        self.client.force_authenticate(user=self.patient)
        response = self.client.get('/appointments/', {"status": "Completed"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only the completed appointment
