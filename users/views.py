from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from users.forms import UserUpdateForm, UserCreateForm


class RegisterView(View):

    def get(self, request):
        create_form = UserCreateForm()
        context = {
            'form': create_form 
        }
        return render(request, 'users/register.html', context)
    
    def post(self, request):
        create_form = UserCreateForm(data=request.POST, files=request.FILES)
        if create_form.is_valid():
            create_form.save()
            return redirect('users:login')
        else:
            context = {
                "form": create_form
            }
            return render(request, 'users/register.html', context)

        
class LoginView(View):

    def get(self, request):
        login_form = AuthenticationForm()  # Django AuthenticationFormdan login uchun foydalandik forma kerakli validatsiyalarni qo'yib beradi
        return render(request, 'users/login.html', {'form': login_form})
    
    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()  # validatsiya qilingan datadan request userni olish
            login(request, user)   # django login function
            messages.success(request, "You are successfully login.")
            return redirect('lending_page')
        else:
            return render(request, 'users/login.html', {'form': login_form})
        

class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        """Login qilingan yoki yuqligini tekshirish uchuun yozilgandi buning o'rniga LoginrequiredMixin"""
        return render(request, 'users/profile.html', {'user': request.user })
        # if request.user.is_authenticated:
        #     return render(request, 'users/profile.html', {'user': request.user })
        # return redirect('users:login')
    

class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.info(request, "You are successfully logout.")
        return redirect('users:login')
    

class ProfileEditView(LoginRequiredMixin, View):

    def get(self, request):
        user_update_form = UserUpdateForm(instance=request.user)

        return render(request, 'users/profile_edit.html', {'form': user_update_form})
    
    def post(self, request):
        user_update_form = UserUpdateForm(
            instance=request.user, 
            data=request.POST, 
            files=request.FILES
            )

        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, "Profile updated successfully!")

            return redirect('users:profile')
        
        messages.warning(request, "Profile updated unsuccessfully!")
        return render(request, 'users/profile_edit.html', {'form': user_update_form})
