from django import forms
from core.models import Order


class CheckOutForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    address = forms.CharField(max_length=255)
    first_name = forms.CharField(max_length=255)
    zipcode = forms.CharField(max_length=255)
    place = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=255)

    class Meta:
        fields = [
            'first_name',
            'last_name',
            'email',
            'address',
            'zipcode',
            'place',
            'phone',
        ]