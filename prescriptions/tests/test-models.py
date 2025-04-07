from django.test import TestCase
from users.models import User
from records.models import MedicalRecord
from prescriptions.models import Prescription, InsuranceClaim
from datetime import date
from decimal import Decimal

class PrescriptionModelTest(TestCase):
    def setUp(self):
        self.doctor = User.objects.create_user(username="doctor", password="pass", is_staff=True, role="doctor")
        self.patient = User.objects.create_user(username="patient", password="pass", is_staff=False, role="patient")

        self.medical_record = MedicalRecord.objects.create(
            patient_id=self.patient,
            doctor_id=self.doctor,
            diagnosis="Flu",
            treatment="Rest"
        )

    def test_create_valid_prescription(self):
        prescription = Prescription.objects.create(
            record_id=self.medical_record,
            prescribed_by=self.doctor,
            patient_id=self.patient,
            medical_details="Paracetamol",
            dosage="500mg",
            frequency="Twice a day",
            duration="5 days"
        )
        self.assertEqual(str(prescription), f"Prescription for {self.patient} - Paracetamol")

    def test_invalid_prescribed_by_non_staff(self):
        non_doctor = User.objects.create_user(username="nonstaff", password="pass", is_staff=False, role="patient")
        with self.assertRaises(Exception):
            Prescription.objects.create(
                record_id=self.medical_record,
                prescribed_by=non_doctor,
                patient_id=self.patient,
                medical_details="Ibuprofen",
                dosage="200mg",
                frequency="Once",
                duration="3 days"
            )


class InsuranceClaimModelTest(TestCase):
    def setUp(self):
        self.doctor = User.objects.create_user(username="doctor", password="pass", is_staff=True, role="doctor")
        self.patient = User.objects.create_user(username="patient", password="pass", is_staff=False, role="patient")

        self.medical_record = MedicalRecord.objects.create(
            patient_id=self.patient,
            doctor_id=self.doctor,
            diagnosis="Fracture",
            treatment="Plaster"
        )

    def test_create_valid_insurance_claim(self):
        claim = InsuranceClaim.objects.create(
            patient_id=self.patient,
            medical_record_id=self.medical_record,
            claim_amount=Decimal("500.00"),
        )
        self.assertEqual(claim.claim_status, "Submitted")
        self.assertEqual(str(claim), f"Insurance claim {claim.id} - Submitted")

    def test_change_claim_status(self):
        claim = InsuranceClaim.objects.create(
            patient_id=self.patient,
            medical_record_id=self.medical_record,
            claim_amount=Decimal("800.00"),
        )
        claim.claim_status = "Approved"
        claim.save()

        updated_claim = InsuranceClaim.objects.get(pk=claim.pk)
        self.assertEqual(updated_claim.claim_status, "Approved")

    def test_invalid_claim_status(self):
        with self.assertRaises(ValueError):
            InsuranceClaim.objects.create(
                patient_id=self.patient,
                medical_record_id=self.medical_record,
                claim_amount=Decimal("300.00"),
                claim_status="InvalidStatus"
            )
