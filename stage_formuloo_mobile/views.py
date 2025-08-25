from rest_framework.views import APIView
from rest_framework.response import Response
from basic_app.models import Tickets, intern_tickets,FormulooUser
from .serializers import TicketSerialiser, intern_tickets_Serializer
from rest_framework.permissions import IsAuthenticated
from .permissions import ScrumMasterPerm
from django.shortcuts import redirect, reverse
import requests

class LoginAPI(APIView):
    def post(self, request):
        host = request.get_host()
        tokens = requests.request(
            'post',
            f"http://{host}{reverse('token_obtain_pair')}",
            data={
                "username": request.POST['username'],
                "password": request.POST['password']
            }
        )
        return Response(tokens.json())

class RegistrationAPI(APIView):
    def post(self, request):
        FormulooUser.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'],
            email=request.POST['email'],
            first_name=request.POST['first_name'],
            role=request.POST['role'],
            Phone_number=request.POST['phone'],
            Picture = request.FILES['picture'] if 'picture' in request.FILES else None
        )
        host = request.get_host()
        tokens= requests.request(
            'post',
            f"http://{host}{reverse('token_obtain_pair')}",
            data={
                "username":request.POST['username'],
                "password":request.POST['password']
            }
        )
        return Response(tokens.json())
class TicketDetailAPI(APIView):

    def get(self,request,pk):
        my_model = Tickets.objects.get(id=pk)
        serializer = TicketSerialiser(my_model)
        return Response(serializer.data)

class TicketAPI(APIView):

    permission_classes = [IsAuthenticated]
    def post(self, request,action,ticket_id=0):
        serializer = TicketSerialiser
        self.permission_classes.append(ScrumMasterPerm)
        if action =="create":
            CreationSerializer=serializer(data=request.data)
            if CreationSerializer.is_valid():
                ticket = CreationSerializer.save()
                return Response(TicketSerialiser(ticket).data)
            else:
                print(CreationSerializer.errors)
                return Response({"error":CreationSerializer.errors})

        try:
            Tickets.objects.get(id=ticket_id)
        except:
            return Response({"error": "no ticket exist with this id"})

        if action == "update":
            ticket = Tickets.objects.get(id=ticket_id)
            UpdateSerializer= TicketSerialiser(ticket, data=request.data, partial=True)
            if UpdateSerializer.is_valid():
                UpdateSerializer.save()
                return Response(UpdateSerializer.data)
            return Response({"error":UpdateSerializer.errors})

        elif action=="destroy":
            Tickets.objects.get(id=ticket_id).delete()
            return Response({"success": f"deleted ticket {ticket_id}"})
        return Response({"error":"invalid action for this request method"})

    def get(self, request,action,ticket_id=0):
        serializer = TicketSerialiser
        if action == "list":
            return Response(serializer(Tickets.objects.all(), many=True).data)


        elif action == "detail":
            my_model = Tickets.objects.get(id=ticket_id)
            return Response(serializer(my_model).data)
        return Response({"error": "invalid action for this request method"})

