from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from users.views import LoginView, LogoutView, ProfileEditView, ProfileView, RegisterView, UserFollowAuthorView, AuthorFollowUserView

app_name = "users"

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change_password/', PasswordChangeView.as_view(template_name="registration/password_change_form.html",
         success_url=reverse_lazy('users:password_change_done')), name='change_password'),
    path('change_password/done', PasswordChangeDoneView.as_view(
        template_name="registration/password_change_done.html"), name='password_change_done'),
    # path('password/reset/', PasswordResetView.as_view(template_name="registration/password_reset.html", email_template_name="registration/password_reset_email.html", success_url='password_reset_done'), name='reset_password'),
    # path('password/reset/done/', PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name='password_reset_done'),
    # path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    # path('password/reset/complete/', PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name='password_reset_complete'),
    # path('password_reset/', PasswordResetView.as_view(template_name='registration/password_reset_form.html',email_template_name='registration/password_reset_email.html',subject_template_name='registration/password_reset_email.txt',success_url='/users/password_reset_done/',from_email='settesla18@gmail.com'), name='password_reset'),
    # path('reset_password/', PasswordResetView.as_view(template_name = "registration/password_reset.html", success_url='password_reset_done'), name ='reset_password'),
    # path('reset_password_sent/', PasswordResetDoneView.as_view(template_name = "registration/reset_password.html"), name ='password_reset_done'),
    # path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name = "registration/password_reset_confirm.html"), name ='password_reset_confirm'),
    # path('reset_password_complete/', PasswordResetCompleteView.as_view(template_name = "registration/password_reset_complete.html"), name ='password_reset_complete'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="registration/reset_password.html", success_url=reverse_lazy('users:password_reset_done')), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_send.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_form.html", success_url=reverse_lazy('users:password_reset_complete')), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_done.html"), name='password_reset_complete'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('profile/followers/', UserFollowAuthorView.as_view(),
         name='user_follow_author'),
    path('author/followers/', AuthorFollowUserView.as_view(), 
        name='author_follow_user'),
]
