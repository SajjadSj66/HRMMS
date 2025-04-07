import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from prescriptions.models import Prescription, InsuranceClaim
from records.models import MedicalRecord
from users.models import User
from datetime import date

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def doctor(django_user_model):
    return django_user_model.objects.create_user(username="doctor1", password="pass123", role="doctor", is_staff=True)

@pytest.fixture
def patient(django_user_model):
    return django_user_model.objects.create_user(username="patient1", password="pass123", role="patient", is_staff=False)

@pytest.fixture
def medical_record(patient, doctor):
    return MedicalRecord.objects.create(patient_id=patient, doctor_id=doctor, diagnosis="test", treatment="test")

@pytest.mark.django_db
def test_prescription_get_as_doctor(api_client, doctor, patient, medical_record):
    api_client.force_authenticate(user=doctor)
    Prescription.objects.create(
        prescribed_by=doctor,
        patient_id=patient,
        record_id=medical_record,
        medical_details="Paracetamol",
        dosage="500mg",
        frequency="2x a day",
        duration="5 days"
    )
    response = api_client.get("/api/prescriptions/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

@pytest.mark.django_db
def test_prescription_post_success(api_client, doctor, patient, medical_record):
    api_client.force_authenticate(user=doctor)
    data = {
        "record_id": medical_record.id,
        "patient_id": patient.id,
        "medical_details": "Ibuprofen",
        "dosage": "200mg",
        "frequency": "3x a day",
        "duration": "7 days"
    }
    response = api_client.post("/api/prescriptions/", data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Prescription.objects.count() == 1

@pytest.mark.django_db
def test_prescription_post_invalid_patient(api_client, doctor, medical_record):
    api_client.force_authenticate(user=doctor)
    # Invalid patient id
    data = {
        "record_id": medical_record.id,
        "patient_id": 9999,
        "medical_details": "Ibuprofen",
        "dosage": "200mg",
        "frequency": "3x a day",
        "duration": "7 days"
    }
    response = api_client.post("/api/prescriptions/", data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_insurance_claim_post_success(api_client, patient, medical_record):
    api_client.force_authenticate(user=patient)
    data = {
        "medical_record_id": medical_record.id,
        "claim_amount": "200.00",
        "claim_status": "Submitted",
        "notes": "Emergency treatment"
    }
    response = api_client.post("/api/insurance-claims/", data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert InsuranceClaim.objects.count() == 1

@pytest.mark.django_db
def test_insurance_claim_get_filter(api_client, patient, medical_record):
    api_client.force_authenticate(user=patient)
    InsuranceClaim.objects.create(
        medical_record_id=medical_record,
        patient_id=patient,
        claim_amount=150.00,
        claim_status="Approved"
    )
    url = "/api/insurance-claims/?claim_status=Approved"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
