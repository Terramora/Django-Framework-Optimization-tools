import hashlib
import random

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import User, UserProfile
from django import forms

CSS_CLASS_AUTH = 'form-control py-4'


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': CSS_CLASS_AUTH,
        'placeholder': 'Введите имя пользователя:'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': CSS_CLASS_AUTH,
        'placeholder': 'Введите пароль:'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': CSS_CLASS_AUTH,
        'placeholder': 'Введите имя пользователя'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': CSS_CLASS_AUTH,
        'placeholder': 'Введите email'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': CSS_CLASS_AUTH,
        'placeholder': 'Введите имя пользователя'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': CSS_CLASS_AUTH,
        'placeholder': 'Введите фамилию пользователя'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': CSS_CLASS_AUTH,
        'placeholder': 'Введите пароль пользователя'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': CSS_CLASS_AUTH,
        'placeholder': 'Подтвердите пароль пользователя'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.active_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': CSS_CLASS_AUTH,
        'readonly': True
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': CSS_CLASS_AUTH,
        'readonly': True
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': CSS_CLASS_AUTH
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': CSS_CLASS_AUTH
    }))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input'
    }), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar')


class UserProfileEdit(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('tagline', 'about', 'gender')

    def __init__(self, *args, **kwargs):
        super(UserProfileEdit, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
