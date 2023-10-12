from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
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



        
class BookReviewtestCase(TestCase):

    def test_add_review(self):
        book = Book.objects.create(
            title='Book 1', 
            description='Book 1 description', 
            isbn='35646383'
            )
        user = CustomUser.objects.create(
            username='temur', 
            first_name='Temurbek', 
            last_name='Yorkulov', 
            email='temur@gmail.com'
            )
        user.set_password('password1234')
        user.save()
        
        self.client.login(username='temur', password='password1234')
        
        self.client.post(reverse('books:review', kwargs={'pk': book.pk}),
            data = {
                'stars_given': 3,
                'comment': 'Nice book'
            }
        )
        book_review = book.reviews.all()

        self.assertEqual(book_review.count(), 1)
        self.assertEqual(book_review[0].stars_given, 3)
        self.assertEqual(book_review[0].comment, 'Nice book')
        self.assertEqual(book_review[0].book, book)
        self.assertEqual(book_review[0].user, user)



    def test_edit_review(self):
        book = Book.objects.create(
            title='Book 1', 
            description='Book 1 description', 
            isbn='35646383'
            )
        user = CustomUser.objects.create(
            username='temur', 
            first_name='Temurbek', 
            last_name='Yorkulov', 
            email='temur@gmail.com'
            )
        user.set_password('password1234')
        user.save()

        self.client.login(username='temur', password='password1234')

        self.client.post(reverse('books:review', kwargs={'pk': book.pk}),
            data = {
                'stars_given': 3,
                'comment': 'Nice book'
            }
        )
        book_review = book.reviews.all()
        review = book_review[0]

        response = self.client.post(reverse('books:review_edit', kwargs={'book_pk': book.pk, 'review_pk': review.pk}), 
                         data = {
                             'stars_given': 4,
                             'comment': 'Very nice book'
                         })
        
        review.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(review.stars_given, 4)
        self.assertEqual(review.comment, 'Very nice book')
        self.assertEqual(response.url, reverse('books:detail', kwargs={'pk': book.pk}))



    def test_delete_confirm_review(self):
        book = Book.objects.create(
            title='Book 1', 
            description='Book 1 description', 
            isbn='35646383'
            )
        user = CustomUser.objects.create(
            username='temur', 
            first_name='Temurbek', 
            last_name='Yorkulov', 
            email='temur@gmail.com'
            )
        user.set_password('password1234')
        user.save()

        self.client.login(username='temur', password='password1234')

        self.client.post(reverse('books:review', kwargs={'pk': book.pk}),
            data = {
                'stars_given': 3,
                'comment': 'Nice book'
            }
        )

        book_review = book.reviews.all()
        review = book_review[0]

        response = self.client.get(reverse('books:review_confirm_delete', kwargs={'book_pk': book.pk, 'review_pk': review.pk}))

        self.assertEqual(response.status_code, 200)


    
    def test_delete_review(self):
        book = Book.objects.create(
            title='Book 1', 
            description='Book 1 description', 
            isbn='35646383'
            )
        user = CustomUser.objects.create(
            username='temur', 
            first_name='Temurbek', 
            last_name='Yorkulov', 
            email='temur@gmail.com'
            )
        user.set_password('password1234')
        user.save()

        self.client.login(username='temur', password='password1234')

        self.client.post(reverse('books:review', kwargs={'pk': book.pk}),
            data = {
                'stars_given': 3,
                'comment': 'Nice book'
            }
        )

        book_review = book.reviews.all()
        review = book_review[0]

        response = self.client.get(reverse('books:review_delete', kwargs={'book_pk': book.pk, 'review_pk': review.pk}))

        count = book_review.count()

        self.assertEqual(count, 0)
        self.assertFalse(BookReview.objects.filter(pk=review.pk).exists())
