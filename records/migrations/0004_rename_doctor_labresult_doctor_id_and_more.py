# Generated by Django 5.1.7 on 2025-03-24 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0003_labresult_test_result'),
    ]

    operations = [
        migrations.RenameField(
            model_name='labresult',
            old_name='doctor',
            new_name='doctor_id',
        ),
        migrations.RenameField(
            model_name='labresult',
            old_name='patient',
            new_name='patient_id',
        ),
        migrations.RenameField(
            model_name='medicalrecord',
            old_name='doctor',
            new_name='doctor_id',
        ),
        migrations.RenameField(
            model_name='medicalrecord',
            old_name='patient',
            new_name='patient_id',
        ),
    ]
