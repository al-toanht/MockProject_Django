from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, ShippingFee

class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control', 'placeholder': 'Name'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomerProfileForm(forms.ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    locality = forms.CharField(label='Locality', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Locality'}))
    mobile = forms.CharField(label='Mobile', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile'}))
    city = forms.ModelChoiceField(
        label='City', 
        queryset=ShippingFee.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Select a city',
        to_field_name='region'
    )

    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'mobile']
       
    