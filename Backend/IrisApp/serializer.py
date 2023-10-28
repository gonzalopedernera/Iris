from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from .models import Business_Data, CollaboratorAccounts, Services, Clients, calendar, Appointment

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'password')
 
class Business_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business_Data
        fields = ('__all__')

class CollaboratorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollaboratorAccounts
        fields = ('__all__')

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ('__all__')

class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ('__all__')

class calendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = calendar
        fields = ('__all__')

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('__all__')
