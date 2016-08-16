# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import EmailValidator
class UserLoginForm(forms.Form):
    email_valid=EmailValidator(message="Email must a@b.c format")
    email = forms.CharField(required=True , initial='', min_length=5, max_length=20,validators=[email_valid], error_messages={'required': 'Email empty!','max_length':'Email max length is 20!','min_length':'Email min length is 5!'})
    password = forms.CharField(required=True , initial='',error_messages={'required': 'Password empty!'})

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserLoginForm, self).__init__(*args, **kwargs)

class UserRegisterForm(forms.Form):
    email_valid=EmailValidator(message="Email must a@b.c format")
    email = forms.CharField(required=True , initial='', min_length=5, max_length=20,validators=[email_valid], error_messages={'required': 'Email empty!','max_length':'Email max length is 20!','min_length':'Email min length is 5!'})
    password = forms.CharField(required=True ,min_length=8, initial='',error_messages={'required': 'Password empty!','min_length':'Password min length is 8!'})
    re_password = forms.CharField(required=True , min_length=8,initial='',error_messages={'required': 'Re-Password empty!','min_length':'Re-Password min length is 8!'})
    phone= forms.CharField(required=True ,min_length=8, max_length=11, initial='',error_messages={'required': 'Phone number empty!','max_length':'Phone max length is 11!','min_length':'Phone min length is 8!'})
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserRegisterForm, self).__init__(*args, **kwargs)
    def clean(self):
        password = self.cleaned_data.get("password",None)
        re_password = self.cleaned_data.get("re_password",None)
        if password and re_password and password == re_password:
            return self.cleaned_data
        else:
            raise forms.ValidationError("Passwords is inconsistent")