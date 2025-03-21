from rest_framework import serializers
from .models import *


class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = '__all__'
        read_only_fields = ["user"]
