from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from books.forms import BookReviewForm
from books.models import Book, BookReview



# class BookListView(ListView):
#     model = Book
#     template_name = 'books/books_list.html'
#     queryset = Book.objects.all()
#     context_object_name = 'books'
#     paginate_by = 2


class BookListView(View):

    def get(self, request):
        books = Book.objects.all().order_by('pk')
        search_query = request.GET.get(
            'q',
            '')
        if search_query:
            books = books.filter(title__icontains=search_query)
            
        page_size = request.GET.get('page_size', 2)
        paginator = Paginator(books, page_size)

        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        return render(
            request, 
            'books/books_list.html', 
            {
                'page_obj': page_obj, 
                'books': books,
                'search_query': search_query
            }
        )


# class BookDetailView(DetailView):
#     model = Book
#     template_name = 'books/books_detail.html'
#     context_object_name = 'book'
    # pk_url_kwarg = 'id'  # bizda defaul pk edi nu lekin o'zgartirsa bo'ladi
    

class BookDetailView(View):

    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        review_form = BookReviewForm()
        reviews = book.reviews.all().order_by('-created_at')

        return render(request, 'books/books_detail.html', {'book': book, 'review_form': review_form, 'reviews': reviews})
    

class BookReviewView(View):
    def post(self, request, pk):
        book = Book.objects.get(pk=pk)
        book_review = BookReviewForm(data=request.POST)

        if book_review.is_valid():
            BookReview.objects.create(
                    book = book,
                    user = request.user,
                    stars_given = book_review.cleaned_data['stars_given'],
                    comment = book_review.cleaned_data['comment'],
            )

            return redirect(reverse('books:detail', kwargs={'pk': book.pk}))
        
        else:
            return render(request, 'books/books_detail.html', {'book': book, 'book_review': book_review})
    
    
class   BookReviewEditView(View):

    def get(self, request, book_pk, review_pk):
        book = Book.objects.get(pk=book_pk)
        review = book.reviews.get(pk=review_pk)
        review_form = BookReviewForm(instance=review)

        return render(request, 'books/edit_review.html', {'book': book, 'review': review, 'review_form': review_form})
    
    def post(self, request, book_pk, review_pk):
        book = Book.objects.get(pk=book_pk)
        review = book.reviews.get(pk=review_pk)
        review_form = BookReviewForm(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse('books:detail', kwargs={'pk': book.pk}))

        return render(request, 'books/edit_review.html', {'book': book, 'review': review, 'review_form': review_form})
    

class BookReviewConfirmDeleteView(View):
    
    def get(self, request, book_pk, review_pk):
        book = Book.objects.get(pk=book_pk)
        review = book.reviews.get(pk=review_pk)

        return render(request, 'books/confirm_delete.html', {'book': book, 'review': review})
    

class BookReviewDeleteView(LoginRequiredMixin, View):
    
    def get(self, request, book_pk, review_pk):
        book = Book.objects.get(pk=book_pk)
        review = book.reviews.get(pk=review_pk)
        
        review.delete()
        messages.success(request, "You have successfully deleted this review!")

        return redirect(reverse('books:detail', kwargs={'pk': book.pk}))


    

    
    
