from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic as views, View
from django.contrib.auth import views as auth_views, get_user_model

from event_ticketing_system.web_auth.forms import RegisterUserForm, LoginUserForm, UserProfileEditForm, \
    RechargeBalanceForm

UserModel = get_user_model()


class NotLoggedInMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated


class RegisterUserView(NotLoggedInMixin, views.CreateView):
    template_name = 'accounts/register_page.html'
    form_class = RegisterUserForm

    def get_success_url(self):
        return reverse_lazy('index')


class LoginUserView(NotLoggedInMixin, auth_views.LoginView):
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
    template_name = 'accounts/profile_details_page.html'
    context_object_name = 'user'


class UserDashboardView(views.DetailView):
    template_name = 'accounts/user_dashboard.html'
    model = get_user_model()
    context_object_name = 'user'


@method_decorator(login_required, name='dispatch')
class UserProfileEditView(View):
    template_name = 'accounts/profile_edit.html'

    def get(self, request, *args, **kwargs):
        user_profile_form = UserProfileEditForm(instance=request.user)
        return render(request, self.template_name, {'user_profile_form': user_profile_form})

    def post(self, request, *args, **kwargs):
        user_profile_form = UserProfileEditForm(request.POST, request.FILES, instance=request.user)

        if user_profile_form.is_valid():
            user_profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile_details', pk=request.user.pk)
        else:
            messages.error(request, "Invalid form submission. Please check your inputs.")
            return render(request, self.template_name, {'user_profile_form': user_profile_form})


@method_decorator(login_required, name='dispatch')
class RechargeBalanceView(View):
    template_name = 'accounts/recharge_balance.html'
    form_class = RechargeBalanceForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            recharge_amount = form.cleaned_data['amount']
            user = request.user
            user.balance += recharge_amount
            user.save()

            messages.success(request, f"Successfully recharged {recharge_amount} to your balance.")
            return redirect(self.get_success_url())
        else:
            messages.error(request, "Invalid form submission. Please check the entered amount.")
            return render(request, self.template_name, {'form': form})

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'pk': self.request.user.pk})
