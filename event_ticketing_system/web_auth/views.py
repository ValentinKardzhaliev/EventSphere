from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views, get_user_model

from event_ticketing_system.common.models import Like
from event_ticketing_system.web_auth.forms import RegisterUserForm, LoginUserForm

UserModel = get_user_model()


class RegisterUserView(views.CreateView):
    template_name = 'accounts/register-page.html'
    form_class = RegisterUserForm

    def get_success_url(self):
        return reverse_lazy('index')


class LoginUserView(auth_views.LoginView):
    template_name = 'accounts/login-page.html'
    form_class = LoginUserForm

    def get_success_url(self):
        return reverse_lazy('index')


class LogoutUserView(auth_views.LogoutView):
    pass

    def get_success_url(self):
        return reverse_lazy('index')


def user_likes(request):
    user = request.user
    liked_events = Like.objects.filter(user=user).values_list('event__title', flat=True)

    context = {
        'user': user,
        'liked_events': liked_events,
    }

    return render(request, 'accounts/user_profile.html', context)


class ProfileDetailsView(views.DetailView):
    template_name = 'accounts/profile-details-page.html'
    model = UserModel

    profile_image = static('images/person.png')

    def get_profile_image(self):
        if self.object.profile_picture is not None:
            return self.object.profile_picture
        return self.profile_image

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_image'] = self.get_profile_image()
        return context
