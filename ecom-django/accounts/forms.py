from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

User = get_user_model()


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

    class Meta:
        models = User
        fields = ["username", "password", "remember_me"]


class UserRegisterForm(UserCreationForm):
    phone = PhoneNumberField(
        region="CA",
        widget=PhoneNumberPrefixWidget(
            country_choices=[
                ("NP", "Nepal"),
            ],
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone",
            "shipping_address",
            "place",
            "username",
            "email",
        ]


class CustomUserChangeForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone = PhoneNumberField(region="NP")
    zipcode = forms.CharField()
    shipping_address = forms.CharField()
    place = forms.CharField()

    class Meta:
        fields = [
            "first_name",
            "last_name",
            "phone",
            "zipcode",
            "shipping_address",
            "place",
        ]
