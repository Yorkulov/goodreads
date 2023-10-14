from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator
from books.models import Author, Book, BookReview
from users.models import CustomUser


def custom_404_page(request, exception=None):
    return render(request, '404.html', status=404)

def lending_page(request):
    numbers = "".join(str(x) for x in range(10))
    data = {
        'authors': Author.objects.count(),
        'books': Book.objects.count(),
        'books_review': BookReview.objects.count(),
        'users': CustomUser.objects.count(),
    }
    return render(request, 'landing_page.html', {'numbers': numbers, 'data': data})

def home_page(request):
    book_reviews = BookReview.objects.all().order_by('-created_at')
    
    page_size = request.GET.get('page_size', 10)
    paginator = Paginator(book_reviews, page_size)

    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)


    return render(request, 'home.html', {'book_reviews': book_reviews, 'page_obj': page_obj})