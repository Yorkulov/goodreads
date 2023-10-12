from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from books.models import Book, BookReview
from users.models import CustomUser



class BookReviewAPITestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='temurbek', email='email', first_name='Temurbek')
        self.user.set_password('password1234')
        self.user.save()

        self.client.post(
            reverse('users:login'),
            data = {
                'username': 'temurbek',
                'password': 'password1234'
            }
        )


    def test_book_review_detail(self):
        book = Book.objects.create(title='Book', description='Description 1', isbn='6341287791')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Very good!')

        response = self.client.get(reverse('api:review-detail', kwargs={'pk': br.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['pk'], br.pk)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], 'Very good!')
        self.assertEqual(response.data['book']['pk'], br.book.pk)
        self.assertEqual(response.data['book']['title'], 'Book')
        self.assertEqual(response.data['book']['description'], 'Description 1')
        self.assertEqual(response.data['book']['isbn'], '6341287791')
        self.assertEqual(response.data['user']['pk'], self.user.pk)
        self.assertEqual(response.data['user']['username'], 'temurbek')
        self.assertEqual(response.data['user']['first_name'], 'Temurbek')


    
    def test_book_review_list(self):
        user_two = CustomUser.objects.create(username='yorkullov', email='yorkulov@gmail.com', first_name='Temurbek')
        book = Book.objects.create(title='Book 1', description='Description one', isbn='8746223915')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment='This is beauiful book!')
        br_two = BookReview.objects.create(book=book, user=user_two, stars_given=5, comment='This is big book!')


        response = self.client.get(reverse('api:review-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)
        
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

        self.assertEqual(response.data['results'][0]['pk'], br_two.pk)
        self.assertEqual(response.data['results'][0]['stars_given'], br_two.stars_given)
        self.assertEqual(response.data['results'][0]['comment'], br_two.comment)
        self.assertEqual(response.data['results'][1]['pk'], br.pk)
        self.assertEqual(response.data['results'][1]['stars_given'], br.stars_given)
        self.assertEqual(response.data['results'][1]['comment'], br.comment)



    def test_delete_review(self):
        book = Book.objects.create(title='Book 1', description='Description one', isbn='8746223915')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment='This is beauiful book!')

        response = self.client.delete(reverse('api:review-detail', kwargs={'pk': br.pk}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(pk=br.pk).exists())



    def test_patch_review(self):
        book = Book.objects.create(title='Book 1', description='Description one', isbn='8746223915')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment='This is beauiful book!')

        response = self.client.patch(reverse('api:review-detail', kwargs={'pk': br.pk}), data={'stars_given': 5})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 5)



    def test_put_review(self):
        book = Book.objects.create(title='Book 1', description='Description one', isbn='8746223915')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment='This is beauiful book!')

        response = self.client.put(reverse('api:review-detail', kwargs={'pk': br.pk}), data={'stars_given': 2, 'comment': 'This is book!', 'book_id': book.pk, 'user_id': self.user.pk})
        br.refresh_from_db()
        

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 2)
        self.assertEqual(br.comment, 'This is book!')



    # def test_create_review(self):
    #     book = Book.objects.create(title='Book 1', description='Description one', isbn='8746223915')
    #     data = {
    #         'stars_given': 4,
    #         'comment': 'This is bookcha',
    #         'user_id': self.user.pk,
    #         'book_id': book.pk
    #     }

    #     response = self.client.post(reverse('api:review-list'), data=data)
    #     br = BookReview.objects.get(book=book)

    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(br.stars_given, 4)
    #     self.assertEqual(br.comment, 'This is bookcha')

                

