from django.urls import path, include
from .views import TicketDetailAPI,RegistrationAPI, LoginAPI, TicketAPI
from rest_framework import routers

# router = routers.SimpleRouter()
# router.register('ticket', TicketAPI, basename='ticket')


urlpatterns = [
    path("api_registration/", RegistrationAPI.as_view(),name="api_registration"),
    path("ticket_api/<str:action>/<int:ticket_id>/",TicketAPI.as_view(), name="ticket_api"),
]