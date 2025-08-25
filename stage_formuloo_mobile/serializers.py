from rest_framework.serializers import ModelSerializer,SerializerMethodField, PrimaryKeyRelatedField, ManyRelatedField
from basic_app.models import Tickets, intern_tickets, FormulooUser

class intern_tickets_Serializer(ModelSerializer):
    user = SerializerMethodField()
    class Meta:
        model = intern_tickets
        fields = ['user','Status']
    def get_user(self, instance):
        return {
            "id":instance.user.id,
            "name":instance.user.username
        }

class TicketSerialiser(ModelSerializer):
    assigned_to = SerializerMethodField()
    # Assignee = PrimaryKeyRelatedField(queryset=FormulooUser.objects.all(), many=True)
    class Meta:
        model = Tickets
        fields = ['id','Name', 'Description', 'Reporter', 'date', 'Image', 'assigned_to']

    def get_assigned_to(self, instance):
        serializer = intern_tickets_Serializer(instance.assigned_to.all(), many=True)
        return serializer.data
    
    # def to_internal_value(self, immutable_data):
    #     data=immutable_data.copy()
    #     if "Assignee" in data and bool(isinstance(data["Assignee"],list) or isinstance(data["Assignee"],str)):
    #         print("convert")
    #         data["Assignee"]=[int(i) for i in data["Assignee"] if not i in ["[","]",",","'", '"', " "] ]
    #     return super().to_internal_value(data)
