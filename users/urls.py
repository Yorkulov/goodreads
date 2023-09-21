from django.urls import path

from users.views import LoginView, LogoutView, ProfileEditView, ProfileView, RegisterView


app_name = "users"   # Tashqi applarda foydalanish uchun
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
]
