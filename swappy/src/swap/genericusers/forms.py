from django import forms
from .models import GenericUser


class LoginForm(forms.ModelForm):
    class Meta:
        model = GenericUser
        fields = ['login', 'user_pass']
        widgets = {
            'login': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'True',
                'max-length': '20',
                'ng-model': 'login.user',
            }),
            'user_pass': forms.PasswordInput(attrs={
                'class': 'form-control',
                'required': 'True',
                'max-length': '20',
                'ng-model': 'login.password',
            }),
        }


class SignupForm(forms.ModelForm):
    class Meta:
        model = GenericUser
        fields = '__all__'
        widgets = {
            'login': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'True',
                'max-length': '20',
                'ng-model': 'signup.user',
            }),
            'user_id': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'True',
                'max-length': '20',
                'ng-model': 'signup.user_id',
            }),
            'user_pass': forms.PasswordInput(attrs={
                'class': 'form-control',
                'required': 'True',
                'max-length': '20',
                'ng-model': 'signup.user_pass',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'True',
                'max-length': '20',
                'ng-model': 'signup.first_name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'True',
                'max-length': '20',
                'ng-model': 'signup.last_name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'required': 'True',
                'max-length': '20',
                'ng-model': 'signup.email',
            }),
            'phone': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': 'True',
                'max-length': '20',
                'ng-model': 'signup.phone',
            }),
        }