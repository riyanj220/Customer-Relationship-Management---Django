from django.shortcuts import render ,redirect

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView ,DeleteView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login

from .forms import CreateUserForm,LoginForm ,AddRecord,UpdateRecord

from django.contrib import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from .models import Record

from django.contrib import messages

class HomeView(TemplateView):
    template_name = "webapp/index.html"


class RegisterView(CreateView):
    form_class = CreateUserForm
    template_name = "webapp/register.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "Account created successfully!")
        return super().form_valid(form)


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'webapp/login.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        return self.success_url
    
    def form_valid(self, form):
        user = authenticate(
            request=self.request,
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
        )
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, "Invalid username or password.")
            return self.form_invalid(form)


class DashboardView(LoginRequiredMixin, ListView):
    model = Record
    template_name = 'webapp/dashboard.html'
    context_object_name = 'records'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return Record.objects.filter(created_by=self.request.user).order_by('-creation_date')
    

class RecordCreateView(LoginRequiredMixin, CreateView):
    form_class = AddRecord
    template_name = 'webapp/create_record.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Record created successfully!")
        return super().form_valid(form)


class RecordUpdateView(LoginRequiredMixin, UpdateView):
    model = Record
    form_class = UpdateRecord
    template_name = 'webapp/update_record.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, "Record updated successfully!")
        return super().form_valid(form)


class RecordDetailView(LoginRequiredMixin, DetailView):
    model = Record
    template_name = 'webapp/view_record.html'
    context_object_name = 'record'


class RecordDeleteView(LoginRequiredMixin, DeleteView):
    model = Record
    success_url = reverse_lazy('dashboard')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Record deleted!")
        return redirect(self.success_url)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "Account logged out!")
        return response
