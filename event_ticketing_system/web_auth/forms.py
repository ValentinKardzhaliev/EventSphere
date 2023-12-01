from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

UserModel = get_user_model()


# forms.py

class RegisterUserForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'custom-form-control', 'style': 'width: 150px'}),
            'email': forms.EmailInput(attrs={'class': 'custom-form-control', 'style': 'width: 150px'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Override widget templates for password fields
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'custom-form-control', 'style': 'width: 150px'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'custom-form-control', 'style': 'width: 150px'})


class LoginUserForm(auth_forms.AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'custom-form-control'}),
        label="Username",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'custom-form-control'}),
        label="Password",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Override widget templates for username and password fields
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'custom-form-control', 'style': 'width: 150px'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'custom-form-control', 'style': 'width: 150px'})
