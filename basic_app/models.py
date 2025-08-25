from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class FormulooUser(AbstractUser):
    Role = (('scrum_master', 'SCRUM_MASTER'),('intern','INTERN'))
    Phone_number = models.IntegerField()
    Picture = models.ImageField(upload_to='profile_picture', null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role)

class Tickets(models.Model):
    Name = models.CharField(max_length=30)
    Description = models.TextField()
    Assignee = models.ManyToManyField(FormulooUser, through='intern_tickets')
    Reporter = models.ForeignKey(FormulooUser, on_delete=models.CASCADE, related_name='tickets_assigned')
    Image = models.ImageField(upload_to='ticket_images', null=True, blank=True)
    date = models.DateTimeField(default=now)



class intern_tickets(models.Model):
    States = (
        ('in_progress', 'IN PROGRESS'),
        ('to_do', 'TO BE DONE'),
        ('done', 'COMPLETED')
    )
    user = models.ForeignKey(FormulooUser, on_delete=models.CASCADE, related_name="my_tickets")
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE, related_name="assigned_to")
    Status = models.CharField(max_length=50, choices=States, default="in_progress")