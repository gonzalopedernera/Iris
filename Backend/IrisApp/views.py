from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import Business_DataSerializer, CollaboratorsSerializer, ServicesSerializer, AppointmentSerializer
from .models import Business_Data, CollaboratorAccounts, Services, Appointment
from datetime import datetime

class Business_DataView(viewsets.ModelViewSet):
    serializer_class = Business_DataSerializer
    queryset = Business_Data.objects.all()

class CollaboratorsView(viewsets.ModelViewSet):
    serializer_class = CollaboratorsSerializer
    queryset = CollaboratorAccounts.objects.all()

class ServicesView(viewsets.ModelViewSet):
    serializer_class = ServicesSerializer
    queryset = Services.objects.all()

class CreateAppointmentView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_service = request.data.get('id_service', None)
        id_collaborator = request.data.get('id_collaborator', None)
        day = request.data.get('days', None)
        selected_time = request.data.get('startTime', None)
        if id_service is None or id_collaborator is None:
            return Response({'error': 'Se requieren los IDs: servicio y colaborador'}, status=status.HTTP_400_BAD_REQUEST)
        if day is None:
            return Response({'error': 'Se requiere el día'}, status=status.HTTP_400_BAD_REQUEST)
        if selected_time is None:
            return Response({'error': 'Se requiere la hora'}, status=status.HTTP_400_BAD_REQUEST)
        # Validar formato de hora (HH:MM sin segundos ni microsegundos)
        try:
            parsed_time = datetime.strptime(selected_time, '%H:%M').time()
        except ValueError:
            return Response({'error': 'Formato de hora inválido'}, status=status.HTTP_400_BAD_REQUEST)
        # Validar si la hora está en incrementos de 30 minutos
         # Validar si la hora está en incrementos de 30 minutos y entre las 8:00 y las 18:00
        if parsed_time.minute % 30 != 0 or not (8 <= parsed_time.hour < 18):
            return Response({'error': 'La hora debe estar en incrementos de 30 minutos y entre las 8:00 y las 18:00'}, status=status.HTTP_400_BAD_REQUEST)
        # Verificar disponibilidad del horario seleccionado
        existing_appointment = Appointment.objects.filter(id_collaborator=id_collaborator, days=day, startTime=selected_time)
        if existing_appointment.exists():
            return Response({'error': 'El horario seleccionado ya está ocupado.'}, status=status.HTTP_400_BAD_REQUEST)
        # Guardar la cita en la base de datos
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class FilteredAppointmentsView(APIView):
    def get(self, request, *args, **kwargs):
        collaborator_id = request.query_params.get('collaborator_id')
        day = request.query_params.get('day')
        if collaborator_id is None or day is None:
            return Response({'error': 'Se requiere el ID del colaborador y el día.'}, status=400)
        try:
            appointments = Appointment.objects.filter(id_collaborator=collaborator_id, days=day)
            serializer = AppointmentSerializer(appointments, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
class CollaboratorsByServiceView(APIView):
    def get(self, request, service_id, *args, **kwargs):
        service = get_object_or_404(Services, id=service_id)
        collaborators = service.id_collaborator.all()
        serializer = CollaboratorsSerializer(collaborators, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

       
"""class CollaboratorsByServiceView(APIView):
    def get(self, request, *args, **kwargs):
        service_id = kwargs.get('service_id')
        if service_id is None:
            return Response({'error': 'Se requiere el ID del servicio.'}, status=400)
        try:
            collaborators = CollaboratorAccounts.objects.filter(services__id=service_id)
            serializer = CollaboratorsSerializer(collaborators, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)"""

"""class ClientsView(viewsets.ModelViewSet):
    serializer_class = ClientsSerializer
    queryset = Clients.objects.all()"""
