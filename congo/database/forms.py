from django import forms
from django.forms import extras
from .models import *


class registered_user_form(forms.ModelForm):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
    date_of_birth = forms.DateField(widget=extras.SelectDateWidget(years=range(1900,2017)))
    class Meta:
        model = RegisteredUser
        fields = ['name',
                  'date_of_birth',
                  'gender',
                  'phone_number',
                  'annual_income']

'''
class user_form(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','password']
'''
class supplier_form(forms.ModelForm):

    class Meta:
        model = supplier
        fields = [
            'supplier_id',
            'company_name',
            'address',
            'phone_number',
            'category',
            'revenue'
        ]