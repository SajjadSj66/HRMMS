from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import User
from records.models import *
from datetime import date
import uuid


class MedicalRecordTest(TestCase):
    def setUp(self):
        self.patient = User.objects.create_user(username="patient", password="testpassword", is_staff=False)
        self.doctor = User.objects.create_user(username="doctor", password="testpassword", is_staff=True)

    def test_medical_record_valid(self):
        record = MedicalRecord.objects.create(
            patient_id=self.patient,
            doctor_id=self.doctor,
            diagnosis="diagnosis test",
            treatment="treatment test",
        )
        self.assertEqual(str(record), f"Record for {self.patient} - {record.record_date}")

    def test_medical_record_invalid_patient_is_staff(self):
        invalid_patient = User.objects.create_user(username='invalid_patient', is_staff=True)
        record = MedicalRecord(
            patient_id=invalid_patient,
            doctor_id=self.doctor,
            diagnosis="x",
            treatment="y",
        )
        with self.assertRaises(ValidationError):
            record.clean()

    def test_medical_record_invalid_doctor_not_staff(self):
        invalid_doctor = User.objects.create_user(username='invalid_doctor', is_staff=False)
        record = MedicalRecord(
            patient_id=self.patient,
            doctor_id=invalid_doctor,
            diagnosis="x",
            treatment="y",
        )
        with self.assertRaises(ValidationError):
            record.clean()


class LabResultModelTest(TestCase):
    def setUp(self):
        self.patient = User.objects.create_user(username="lab_patient", password="testpassword", is_staff=False)
        self.doctor = User.objects.create_user(username="lab_doctor", password="testpassword", is_staff=True)

    def test_set_and_get_test_result(self):
        lab_result = LabResult.objects.create(
            patient_id=self.patient,
            doctor_id=self.doctor,
            test_name="Blood Test",
            normal_range="4.0-6.0",
            test_date=date.today(),
            external_ref=str(uuid.uuid4()),
        )
        lab_result._test_result = "Test Result"
        lab_result.save()

        retrieved = LabResult.objects.get(pk=lab_result.pk)
        self.assertEqual(retrieved._test_result, "Test Result")

    def test_duplicate_external_ref_raise_error(self):
        ext_ref = str(uuid.uuid4())

        LabResult.objects.create(
            patient_id=self.patient,
            doctor_id=self.doctor,
            test_name="Test A",
            normal_range="Range",
            test_date=date.today(),
            external_ref=ext_ref,
        )

        with self.assertRaises(Exception):
            LabResult.objects.create(
                patient_id=self.patient,
                doctor_id=self.doctor,
                test_name="Test B",
                normal_range="Range",
                test_date=date.today(),
                external_ref=ext_ref,
            )
