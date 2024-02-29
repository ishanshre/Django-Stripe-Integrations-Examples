from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse

from accounts.forms import UserLoginForm, UserRegisterForm, CustomUserChangeForm

# Create your views here.


class UserLoginView(LoginView):
    template_name = "user/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("core:index")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:index")
        return super().dispatch(request, *args, **kwargs)


class UserRegisterView(CreateView):
    template_name = "user/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("core:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:index")
        return super().dispatch(request, *args, **kwargs)


@login_required
def myAccount(request):
    form = CustomUserChangeForm()

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.phone = form.cleaned_data["phone"]
            user.zipcode = form.cleaned_data["zipcode"]
            user.shipping_address = form.cleaned_data["shipping_address"]
            user.place = form.cleaned_data["place"]
            user.save()
            return redirect("core:myaccount")
    else:
        form = CustomUserChangeForm()

    return render(request, "user/myaccount.html", context={"form": form})
