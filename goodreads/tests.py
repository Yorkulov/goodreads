

from django.test import TestCase
from django.urls import reverse
from books.models import Book, BookReview

from users.models import CustomUser


class HomePageViewTest(TestCase):

    def test_all_review(self):
        book1 = Book.objects.create(title='Book 1', description='Book 1 desription', isbn='6375029427')
        
        user = CustomUser.objects.create(username='temur', email='temur@gmail.com')
        user.set_password('password1234')
        user.save()

        review1 = BookReview.objects.create(book=book1, user=user, stars_given=1, comment="It is very beatiful")
        review2 = BookReview.objects.create(book=book1, user=user, stars_given=2, comment="It is very beatiful")
        review3 = BookReview.objects.create(book=book1, user=user, stars_given=3, comment="It is very beatiful")
        review4 = BookReview.objects.create(book=book1, user=user, stars_given=4, comment="It is very beatiful")
        review5 = BookReview.objects.create(book=book1, user=user, stars_given=5, comment="It is very beatiful")

        response = self.client.get(reverse('home_page') + '?page=2')

        self.assertContains(response, review5.stars_given)
        self.assertContains(response, review2.stars_given)
        self.assertContains(response, review3.stars_given)
        self.assertContains(response, review4.stars_given)
        self.assertContains(response, review1.stars_given)
