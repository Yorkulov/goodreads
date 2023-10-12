from django.test import TestCase
from django.contrib.auth import get_user
from django.urls import reverse
from books.models import Author, RequestAuthorUser
from users.models import CustomUser


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        """CustomUser yaratilganini test qiladi"""
        self.client.post(
            reverse('users:register'),
            data = {
                'username': 'temurbek',
                'first_name': 'Temurbek',
                'last_name': 'Yorkulov',
                'email': 'temur1@gmail.com',
                'password': 'password1234'
            })
        
        user = CustomUser.objects.get(username='temurbek')

        self.assertEqual(user.first_name, 'Temurbek')
        self.assertEqual(user.last_name, 'Yorkulov')
        self.assertEqual(user.email, 'temur1@gmail.com')
        self.assertNotEqual(user.password, 'password1234')
        self.assertTrue(user.check_password('password1234'))
    


    def test_required_fields(self):
        """Kiritilishi shart bo'lgan fieldlarni test qiladi"""
        response = self.client.post(
            reverse('users:register'),
            data = {
                'first_name': 'Temurbek',
                'email': 'temur@gmail.com'
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')


    def test_invalid_email(self):
        """Email noto'g'riligini test qiladi"""
        response = self.client.post(
            reverse('users:register'),
            data = {
                'username': 'temurbek',
                'first_name': 'Temurbek',
                'last_name': 'Yorkulov',
                'email': 'invalid-email',
                'password': 'password'
            }
        )

        user_count = CustomUser.objects.count()
        
        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')


    def test_unique_username(self):
        """Testimiz vazifasi username malumotlar bazasida mavjud yoki yuqligini tekshirib beradi"""
        user = CustomUser.objects.create(username='temurbek', first_name='Temurbek')
        user.set_password('password1234')
        user.save()


        response = self.client.post(
            reverse('users:register'),
            data = {
                'username': 'temurbek',
                'first_name': 'Ali',
                'last_name': 'Vali',
                'email': 'ali1@gmail.com',
                'password': 'password1234'
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')


    def test_unique_email(self):
        """Testimiz vazifasi email malumotlar bazasida avval kiritilgan yoki yuqligini tekshirib beradi"""
        user = CustomUser.objects.create(username='temur', email='temur@gmail.com')
        user.set_password('password1234')
        user.save()

        response = self.client.post(
            reverse('users:register'),
            data = {
                'username': 'temurbek',
                'first_name': 'Temurbek',
                'last_name': 'Yorkulov',
                'email': 'temur@gmail.com',
                'password': 'password1234'
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 1)
        self.assertFormError(response, 'form', 'email', 'This email already used!')



class LoginTestCase(TestCase):

    def setUp(self):
        # DRF - Dont repeat yourself
        self.db_user = CustomUser.objects.create(username='temurbek', email='ytemur@gmail.com')
        self.db_user.set_password('password1234')
        self.db_user.save()

    def test_login_successfully(self):
        """Login muvaffaqiyatli amalga oshirilganligini test qilish"""
        # db_user = CustomUser.objects.create(username='temurbek', email='ytemur@gmail.com')
        # db_user.set_password('password1234')
        # db_user.save()

        self.client.post(
            reverse('users:login'),
            data = {
                'username': 'temurbek',
                'password': 'password1234'
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)


    def test_wrong_login(self):
        # db_user = CustomUser.objects.create(username='temurbek', email='ytemur@gmail.com')
        # db_user.set_password('password1234')
        # db_user.save()

        self.client.post(
            reverse('users:login'),
            data = {
                'username': 'temur',
                'password': 'password1234'
            }
        )
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

        
        self.client.post(
            reverse('users:login'),
            data = {
                'username': 'temurbek',
                'password': 'password123'
            }
        )
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)


    def test_logout(self):
        # db_user = CustomUser.objects.create(username='temurbek', password='password1234')
        # db_user.set_password('password1234')
        # db_user.save()

        self.client.login(username='temurbek', password='password1234')

        self.client.get(reverse('users:logout'))

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)



class ProfileTestCase(TestCase):

    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login') + '?next=/users/profile/')


    def test_profile_details(self):
        user = CustomUser.objects.create(username='temurbek', first_name='Temurbek', last_name='Yorkulov', email='temur@gmail.com')
        user.set_password('password1234')
        user.save()

        self.client.login(username='temurbek', password='password1234')

        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)


    def test_update_profile(self):
        user = CustomUser.objects.create(
            username='temurbek', 
            first_name='Temurbek', 
            last_name='Yorkulov', 
            email='temur@gmail.com'
        )

        user.set_password('password1234')
        user.save()

        self.client.login(username='temurbek', password='password1234')

        response = self.client.post(
            reverse('users:profile_edit'),
            data={
                'username': 'temurbek',
                'first_name': 'Temur',
                'last_name': 'Yorkulov',
                'email': 'yorkulov@gmail.com'
            }
        )
        
        user.refresh_from_db()

        self.assertEqual(user.username, 'temurbek')
        self.assertEqual(user.first_name, 'Temur')
        self.assertEqual(user.last_name, 'Yorkulov')
        self.assertEqual(user.email, 'yorkulov@gmail.com')
        self.assertEqual(response.url, reverse('users:profile'))



# class UserFollowAuthorTestCase(TestCase):
    
#     def test_request_author_user_get(self):

#         user = CustomUser.objects.create(
#             username='temurbek', 
#             first_name='Temurbek', 
#             last_name='Yorkulov', 
#             email='temur@gmail.com'
#         )

#         user.set_password('password1234')
#         user.save()
#         self.client.login(username='temurbek', password='password1234')

#         author = Author.objects.create(
#             first_name = 'Temurbek',
#             last_name = 'Yorkulov',
#             email = 'Yorkulov@gmail.com',
#             bio = "He is very good author!",
#         )

#         request_ = RequestAuthorUser.objects.create(
#             user = user,
#             author = author,
#             is_status = True,
#         )

#         response = self.client.get(reverse('users:user_follow_author'))

#         self.assertEqual(response.status_code, 200)