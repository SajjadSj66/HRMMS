# Generated by Django 5.1.7 on 2025-03-13 20:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('records', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InsuranceClaim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claim_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('claim_status', models.CharField(choices=[('Submitted', 'Submitted'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Submitted', max_length=20)),
                ('submitted_date', models.DateField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('medical_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insurance_claims', to='records.medicalrecord')),
                ('patient', models.ForeignKey(limit_choices_to={'is_staff': False}, on_delete=django.db.models.deletion.CASCADE, related_name='insurance_claims', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medical_details', models.CharField(max_length=255)),
                ('dosage', models.CharField(max_length=100)),
                ('frequency', models.CharField(max_length=100)),
                ('duration', models.CharField(max_length=100)),
                ('notes', models.TextField(blank=True, null=True)),
                ('issued_date', models.DateField(auto_now_add=True)),
                ('medical_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='records.medicalrecord')),
                ('patient', models.ForeignKey(limit_choices_to={'is_staff': True}, on_delete=django.db.models.deletion.CASCADE, related_name='patient_prescriptions', to=settings.AUTH_USER_MODEL)),
                ('prescribed_by', models.ForeignKey(limit_choices_to={'is_staff': True}, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_prescriptions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
