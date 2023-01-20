from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from accounts.forms import UserLoginForm, UserRegisterForm
# Create your views here.


class UserLoginView(LoginView):
    template_name = 'user/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('core:index')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:index')
        return super().dispatch(request, *args, **kwargs)


class UserRegisterView(CreateView):
    template_name = 'user/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('core:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:index')
        return super().dispatch(request, *args, **kwargs)


