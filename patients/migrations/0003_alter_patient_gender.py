# Generated by Django 5.1.7 on 2025-04-21 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Child', 'Child')], default='Male', max_length=10),
        ),
    ]
