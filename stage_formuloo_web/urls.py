from django.urls import path
from .views import home_view,logout_view, RegistrationView, LoginView, CreateTicket, DeleteTicket,DetailTicket, ListTickets, UpdateTicket


urlpatterns = [
    path("home/", home_view, name="home"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    path('logout/',logout_view, name="logout"),
    path("create_ticket/", CreateTicket.as_view(), name="create_ticket"),
    path("delete_ticket/<int:pk>/", DeleteTicket.as_view(), name="delete_ticket"),
    path("ticket_detail/<int:pk>/",DetailTicket.as_view(), name="ticket_detail"),
    path("ticket_list/", ListTickets.as_view(), name="ticket_list"),
    path("update_ticket/<int:pk>/", UpdateTicket.as_view(), name = "update_ticket")
]