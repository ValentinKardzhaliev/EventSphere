from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

UserModel = get_user_model()


class RegisterUserForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'custom-form-control'}),
            'email': forms.EmailInput(attrs={'class': 'custom-form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'custom-form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'custom-form-control'}),
        }


class LoginUserForm(auth_forms.AuthenticationForm):
    class Meta:
        widgets = {
            'username': forms.TextInput(attrs={'class': 'custom-form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'custom-form-control'}),
        }
