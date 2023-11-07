from django.urls import path, include

urlpatterns = [
    path('jwt/create/', include('djoser.urls.jwt')),
]
