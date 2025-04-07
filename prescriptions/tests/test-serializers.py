import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from prescriptions.serializers import PrescriptionSerializer, InsuranceClaimSerializer
from prescriptions.models import Prescription, InsuranceClaim
from records.models import MedicalRecord

User = get_user_model()


@pytest.fixture
def doctor(db):
    return User.objects.create_user(username="doctor", password="pass", role="doctor", is_staff=True)


@pytest.fixture
def patient(db):
    return User.objects.create_user(username="patient", password="pass", role="patient", is_staff=False)


@pytest.fixture
def medical_record(db, doctor, patient):
    return MedicalRecord.objects.create(
        doctor_id=doctor,
        patient_id=patient,
        diagnosis="Diagnosis",
        treatment="Treatment"
    )


@pytest.fixture
def serializer_context(doctor, rf):
    request = rf.post("/")
    request.user = doctor
    return {"request": request}


def test_create_prescription_valid(serializer_context, medical_record, patient):
    data = {
        "record_id": medical_record.id,
        "patient_id": patient.id,
        "medical_details": "Medicine A",
        "dosage": "1 tablet",
        "frequency": "Twice a day",
        "duration": "7 days"
    }
    serializer = PrescriptionSerializer(data=data, context=serializer_context)
    assert serializer.is_valid(), serializer.errors
    prescription = serializer.save()
    assert prescription.prescribed_by == serializer_context["request"].user
    assert prescription.patient_id == patient


def test_prescription_invalid_user_role(patient, medical_record, rf):
    request = rf.post("/")
    request.user = patient
    context = {"request": request}
    data = {
        "record_id": medical_record.id,
        "patient_id": patient.id,
        "medical_details": "Medicine A",
        "dosage": "1 tablet",
        "frequency": "Twice a day",
        "duration": "7 days"
    }
    serializer = PrescriptionSerializer(data=data, context=context)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


def test_prescription_patient_mismatch(doctor, patient, rf, medical_record):
    request = rf.post("/")
    request.user = doctor
    other_patient = User.objects.create_user(username="other", password="pass", role="patient", is_staff=False)
    data = {
        "record_id": medical_record.id,
        "patient_id": other_patient.id,
        "medical_details": "Medicine B",
        "dosage": "1 tab",
        "frequency": "Once",
        "duration": "5 days"
    }
    serializer = PrescriptionSerializer(data=data, context={"request": request})
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


def test_insurance_claim_valid(patient, medical_record, rf):
    request = rf.post("/")
    request.user = patient
    data = {
        "medical_record": medical_record.id,
        "patient": patient.id,
        "claim_amount": "250.00",
        "claim_status": "Submitted"
    }
    serializer = InsuranceClaimSerializer(data=data, context={"request": request})
    assert serializer.is_valid(), serializer.errors
    claim = serializer.save()
    assert claim.claim_status == "Submitted"
    assert claim.patient_id == patient


def test_insurance_claim_invalid_role(doctor, medical_record, rf):
    request = rf.post("/")
    request.user = doctor
    data = {
        "medical_record": medical_record.id,
        "patient": doctor.id,
        "claim_amount": "100.00"
    }
    serializer = InsuranceClaimSerializer(data=data, context={"request": request})
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


def test_insurance_claim_patient_mismatch(patient, medical_record, rf):
    other_patient = User.objects.create_user(username="new_patient", password="pass", role="patient", is_staff=False)
    request = rf.post("/")
    request.user = other_patient
    data = {
        "medical_record": medical_record.id,
        "patient": other_patient.id,
        "claim_amount": "150.00"
    }
    serializer = InsuranceClaimSerializer(data=data, context={"request": request})
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
