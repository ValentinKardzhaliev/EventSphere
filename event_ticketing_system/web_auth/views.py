from django.views import generic as views
from django.contrib.auth import views as auth_views

from event_ticketing_system.web_auth.forms import RegisterUserForm, LoginUserForm


class RegisterUserView(views.CreateView):
    template_name = 'accounts/register-page.html'
    form_class = RegisterUserForm


class LoginUserView(auth_views.LoginView):
    template_name = 'accounts/login-page.html'
    form_class = LoginUserForm


class LogoutUserView(auth_views.LogoutView):
    pass
