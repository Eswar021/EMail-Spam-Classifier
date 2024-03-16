from django import forms


class UserForm(forms.Form):
    Email=forms.CharField(min_length=10)