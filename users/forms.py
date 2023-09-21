from django import forms
from users.models import CustomUser


# class UserCreateForm(forms.Form):  # Form orali foydalanganda barcha fieldlarni yozib chiqishimizga to'g'ri keladi
#     username = forms.CharField(max_length=150)
#     first_name = forms.CharField(max_length=150)
#     last_name = forms.CharField(max_length=150)
#     email = forms.EmailField()
#     password = forms.CharField(max_length=128)

#     def save(self):
#         username = self.cleaned_data['username']
#         first_name = self.cleaned_data['first_name']
#         last_name = self.cleaned_data['last_name']
#         email = self.cleaned_data['email']
#         password = self.cleaned_data['password']

#         user = CustomUser.objects.create(  # yangi obyekt yaratish 
#             username = username,
#             first_name  = first_name,
#             last_name = last_name,
#             email = email
#         )
#         user.set_password(password)  # passwordni bazaga heshlab yozish
#         user.save()  # obyektni bazaga saqlash
#         return user




# Formani ModelFormdagi ko'rinishi
class UserCreateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'profile_picture')

    def clean_email(self):  # nomi o'zgarsa ishlamaskan
        data = self.cleaned_data['email']
        if CustomUser.objects.filter(email=data).exists():
            raise forms.ValidationError('This email already used!')
        
        return data


    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password'])
        user.save()

        return user
        

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_picture')