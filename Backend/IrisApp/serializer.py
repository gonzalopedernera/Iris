from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from .models import Business_Data, CollaboratorAccounts, Services, Appointment

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'password')
class Business_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business_Data
        #fields = ('__all__')
        fields = ('id', 'id_user', 'name_business', 'address', 'phone', 'business_type', 'opening_hours', 'closing_hours')
class CollaboratorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollaboratorAccounts
        fields = ('name', 'email', 'phone', 'id_business_data')
class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ('__all__')
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('__all__')