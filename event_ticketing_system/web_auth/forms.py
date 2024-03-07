from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

UserModel = get_user_model()


# forms.py

class RegisterUserForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'custom-form-control'}),
            'email': forms.EmailInput(attrs={'class': 'custom-form-control' }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Override widget templates for password fields
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'custom-form-control'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'custom-form-control'})


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
        self.fields['username'].widget = forms.TextInput(
            attrs={'class': 'custom-form-control'})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': 'custom-form-control'})


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture'].required = False


class RechargeBalanceForm(forms.Form):
    amount = forms.DecimalField(label='Amount', min_value=0.01)