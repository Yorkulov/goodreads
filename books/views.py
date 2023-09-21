from django.shortcuts import render
from django.views import View

from books.models import Book



class BookListView(View):

    def get(self, request):
        books = Book.objects.all()
        return render(request, 'books/books_list.html', {'books': books})
    

class BookDetailView(View):

    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        return render(request, 'books/books_detail.html', {'book': book})
