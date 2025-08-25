from django import forms
from .models import *

class RegistrationForm(forms.ModelForm):
    class Meta:
        model =FormulooUser
        fields = (
            'username',
            'password',
            'first_name',
            'email',
            'role',
            'Phone_number',
            'Picture'
        )
    def save(self, commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class TicketsForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = (
            'Name',
            'Description',
            'Assignee',
            'Image'
        )


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password")