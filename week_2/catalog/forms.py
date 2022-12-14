from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth import password_validation

from catalog.models import AdvUser, Application
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.ModelForm):
    LetterValidator = RegexValidator(r'^[- а-яА-Я]*$')
    LoginValidator = RegexValidator(r'^[- a-zA-Z]*$')
    username = forms.CharField(validators=[LoginValidator], required=True, label='Логин',
                               help_text='Только латиница и дефис, уникальный')
    fullname = forms.CharField(validators=[LetterValidator], required=True, label='ФИО',
                               help_text='Только кириллические буквы, дефис и пробелы')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    consent = forms.BooleanField(widget=forms.CheckboxInput, required=True,
                                 label='Согласие на обработку персональных данных')

    class Meta:
        model = AdvUser
        fields = ('username', 'fullname', 'email', 'password', 'password2', 'consent')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']

    def clean_password1(self):
        password = self.cleaned_data['password']
        if password:
            password_validation.validate_password(password)
        return password


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'summary', 'category', 'image']


class ApplicationStatusForm(forms.ModelForm):
    comment = forms.CharField(max_length=1000)

    class Meta:
        model = Application
        fields = ['status', 'image', 'comment']
