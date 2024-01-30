from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
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
    def get(self, request, *args, **kwargs):
        messages.success(request, 'You have been logged out successfully.')
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('index')


@method_decorator(login_required, name='dispatch')
class ProfileDetailsView(views.DetailView):
    model = get_user_model()
    template_name = 'accounts/profile_details-page.html'
    context_object_name = 'user'

class UserDashboardView(views.DetailView):
    template_name = 'accounts/user_dashboard.html'
    model = get_user_model()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        # Get the tickets associated with the user
        user_tickets = Ticket.objects.filter(purchase__user=user)

        # Calculate total quantity and add to the context
        user_tickets_quantity = []
        for ticket in user_tickets:
            total_quantity = sum([purchase.quantity for purchase in ticket.purchase_set.filter(user=user)])
            user_tickets_quantity.append({
                'event__title': ticket.event.title,
                'ticket_type': ticket.get_ticket_type_display(),
                'total_quantity': total_quantity,
                'price_per_ticket': ticket.price_per_ticket,
            })

        context['user_tickets_quantity'] = user_tickets_quantity
        return context

