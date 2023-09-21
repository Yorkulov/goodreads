from django.test import TestCase
from django.urls import reverse

from books.models import Book


class BooksTestCase(TestCase):

    def test_books_list_all(self):
        Book.objects.create(title='Book 1', description='Book 1 desription', isbn='637575029427')
        Book.objects.create(title='Book 2', description='Book 2 description', isbn='734286532478675')
        Book.objects.create(title='Book 3', description='Book 3 description', isbn='4126458723129')

        books_count = Book.objects.count()

        self.assertTrue(books_count, 0)

    def test_no_books(self):
        response = self.client.get(reverse('books:list'))

        self.assertContains(response, 'No books found.')

    def test_books_list(self):
        Book.objects.create(title='Book 1', description='Book 2 description', isbn='72346732846')
        Book.objects.create(title='Book 2', description='Book 2 description', isbn='72346732846')
        Book.objects.create(title='Book 3', description='Book 3 description', isbn='72346732846')

        response = self.client.get(reverse('books:list'))

        books = Book.objects.all()
        for book in books:
            self.assertContains(response, book.title)

    def test_detail_page(self):
        book = Book.objects.create(title='Book 1', description='Book 1 description', isbn='7843265243')
        response = self.client.get(reverse('books:detail', kwargs={'pk': book.pk}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
        self.assertContains(response, book.isbn)
        
    