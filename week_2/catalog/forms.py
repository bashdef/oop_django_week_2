from django.contrib.auth.models import User
from django import forms


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    patronymic = forms.CharField(label='Отчество')
    consent = forms.BooleanField(widget=forms.CheckboxInput, required=True, label='Согласие на обработку персональных данных')

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']
