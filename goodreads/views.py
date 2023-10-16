from audioop import reverse
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.core.paginator import Paginator
from django.views import View
from django.contrib import messages
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


class HomePageView(View):
    def get(self, request):
        book_reviews = BookReview.objects.all().order_by('-created_at')
        search_query = request.GET.get('q','')

        if search_query:
            book_reviews = book_reviews.filter(comment__icontains=search_query)

        page_size = request.GET.get('page_size', 10)
        paginator = Paginator(book_reviews, page_size)

        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)
        

        return render(request, 'home.html', {'book_reviews': book_reviews, 'page_obj': page_obj, 'search_query': search_query})
    






