from django.urls import path, include

from event_ticketing_system.web_auth.views import RegisterUserView, LoginUserView, LogoutUserView, ProfileDetailsView, \
    UserDashboardView, UserProfileEditView, RechargeBalanceView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('logout/', LogoutUserView.as_view(), name='logout_user'),
    path('profile/<int:pk>/', include([
        path('', ProfileDetailsView.as_view(), name='profile_details'),
        path('dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
        path('edit/', UserProfileEditView.as_view(), name='profile_edit'),
        path('recharge-balance/', RechargeBalanceView.as_view(), name='recharge_balance'),
        # path('delete/', ProfileDeleteView.as_view(), name='profile delete')
    ]))
]
