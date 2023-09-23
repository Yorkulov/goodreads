from django.test import TestCase
from django.urls import reverse

from books.models import Book
from users.models import CustomUser


class BooksTestCase(TestCase):

    def test_books_list_all(self):
        book1 = Book.objects.create(title='Book 1', description='Book 1 desription', isbn='6375029427')
        book2 = Book.objects.create(title='Book 2', description='Book 2 description', isbn='73425324775')
        book3 = Book.objects.create(title='Book 3', description='Book 3 description', isbn='41264523129')

        response = self.client.get(reverse('books:list'))

        for book in [book1, book2]:
            self.assertContains(response, book.title)

        response = self.client.get(reverse('books:list') + '?page=2')
        self.assertContains(response, book3.title)

        books_count = Book.objects.count()

        self.assertTrue(books_count, 3)


    def test_no_books(self):
        response = self.client.get(reverse('books:list'))

        self.assertContains(response, 'No books found.')



    def test_detail_page(self):
        book1 = Book.objects.create(title='Book 1', description='Book 1 description', isbn='35646383')
        response = self.client.get(reverse('books:detail', kwargs={'pk': book1.pk}))

        self.assertContains(response, book1.title)
        self.assertContains(response, book1.description)
    

    def test_search_books(self):
        book1 = Book.objects.create(title='Sport', description='Book 1 description', isbn='87345623')
        book2 = Book.objects.create(title='Tezlik', description='Book 2 description', isbn='873447323')
        book3 = Book.objects.create(title='Compyuter', description='Book 3 description', isbn='87334563')

        response = self.client.get(reverse('books:list') + '?q=sport')
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + '?q=tezlik')
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + '?q=compyuter')
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)

        
# class BookReviewtestCase(TestCase):
#     def test_add_review(self):
#         book = Book.objects.create(title='Book 1', description='Book 1 description', isbn='35646383')
#         user = CustomUser.objects.create(username='temur', first_name='Temurbek', last_name='Yorkulov', email='temur@gmail.com')
#         user.set_password('password1234')
#         user.save()
        
#         self.client.login(username='temurbek', password='password1234')
        
#         self.client.post(reverse('books:review', kwargs={'pk', book.pk}), data = {
#             'stars_given': 3,
#             'comment': 'Nive book'
#         })
#         book_review = book.reviews.all()

#         self.assertEqual(book_review.count(), 1)
#         self.assertEqual(book_review[0].stars_given, 3)
#         self.assertEqual(book_review[0].comment, 'Nice book')
#         self.assertEqual(book_review[0].book, book)
#         self.assertEqual(book_review[0].user, user)
