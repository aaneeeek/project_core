from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from basic_app.forms import RegistrationForm, TicketsForm, LoginForm
from basic_app.models import FormulooUser, Tickets, intern_tickets
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy


def home_view(request):
    if request.user.is_authenticated and not request.user.is_active:
        request.user.is_active = True
        request.user.save()
    if request.user.is_authenticated and request.user.role == 'scrum_master' and not request.user.is_superuser:
        request.user.is_superuser =True
        request.user.save()
        print("admin")
    print(request.user.is_active)
    return render(request, "home.html")


def logout_view(request):
    logout(request)
    return redirect('home')

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form":form})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username, password)
            user = authenticate(request, username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                return render(request, "login.html", {"form": form, "error":"wrong username or password"})
        return render(request, "login.html", {"form": form, "error": "Unable to login"})

class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "registration_page.html", {"form":form})
    def post(self, request):
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, "registration_page.html", {"form":form, "error":"Unable to sign up"})


class CreateTicket(CreateView, PermissionRequiredMixin):
    model = Tickets
    form_class = TicketsForm
    template_name = "create_ticket.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        print("valid")
        print(self.request.user)
        form.instance.Reporter = self.request.user
        print(form.instance.Reporter)
        print(self.request.FILES)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == 'scrum_master':
            return HttpResponse("YOU ARE NOT AUTHORISED")
        return super().dispatch(request, *args, **kwargs)

class DeleteTicket(DeleteView, PermissionRequiredMixin):
    model = Tickets
    # form_class = TicketsForm
    template_name = "delete_ticket.html"
    success_url = reverse_lazy('home')
    context_object_name = 'ticket'

    def dispatch(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            print(pk)
            self.model.objects.get(id=pk)
            print(pk)
        except:
            return HttpResponse("DOES NOT EXIST")
        if not request.user.role == 'scrum_master':
            return HttpResponse("YOU ARE NOT AUTHORISED")
        return super().dispatch(request, *args, **kwargs)
#
#
class DetailTicket(DetailView, PermissionRequiredMixin):
    model = Tickets
    # form_class = TicketsForm
    template_name = "ticket_detail.html"
    success_url = reverse_lazy('home')
    context_object_name = 'ticket'



    def dispatch(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            print(pk)
            self.model.objects.get(id=pk)
            print(pk)
        except:
            return HttpResponse("DOES NOT EXIST")
        return super().dispatch(request, *args, **kwargs)

#

class ListTickets(ListView):
    model = Tickets
    template_name = "list_ticket.html"
    success_url = reverse_lazy('home')
    context_object_name = 'ticket'
    paginate_by = 5


class UpdateTicket(UpdateView, PermissionRequiredMixin):
    model = Tickets
    form_class = TicketsForm
    template_name = "update_ticket.html"
    success_url = reverse_lazy('home')
    context_object_name = 'ticket'
    def dispatch(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            print(pk)
            self.model.objects.get(id=pk)
            print(pk)
        except:
            return HttpResponse("DOES NOT EXIST")
        if not request.user.role == 'scrum_master':
            return HttpResponse("YOU ARE NOT AUTHORISED")
        return super().dispatch(request, *args, **kwargs)