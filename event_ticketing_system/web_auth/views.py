from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic as views
from django.contrib.auth import views as auth_views, get_user_model

from event_ticketing_system.tickets.models import Ticket
from event_ticketing_system.web_auth.forms import RegisterUserForm, LoginUserForm

UserModel = get_user_model()


class RegisterUserView(views.CreateView):
    template_name = 'accounts/register_page.html'
    form_class = RegisterUserForm

    def get_success_url(self):
        return reverse_lazy('index')


class LoginUserView(auth_views.LoginView):
    template_name = 'accounts/login_page.html'
    form_class = LoginUserForm

    def get_success_url(self):
        return reverse_lazy('index')


class LogoutUserView(auth_views.LogoutView):
    pass

    def get_success_url(self):
        return reverse_lazy('index')


@method_decorator(login_required, name='dispatch')
class ProfileDetailsView(views.DetailView):
    model = get_user_model()
    template_name = 'accounts/profile_details-page.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        # Get the tickets associated with the user
        user_tickets = Ticket.objects.filter(purchase__user=user)

        context['user_tickets'] = user_tickets
        return context


class UserDashboardView(views.TemplateView):
    template_name = 'accounts/user_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Add any additional data you want to display on the user dashboard
        context['user'] = user
        return context
