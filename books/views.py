from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from books.forms import AuthorForm, AuthorUserChatForm, BookForm, BookReviewForm, MessageToAuthorForm, RequestAuthorUserForm
from books.models import Author, Book, BookAuthor, BookReview, MessageToAuthor, RequestAuthorUser
from users.models import CustomUser


class AuthorView(View):
    def post(self, request, pk):
        author = Author.objects.get(pk=pk)
        user = CustomUser.objects.get(pk=self.request.user.pk)        

        request_form = RequestAuthorUser.objects.filter(author=author, user=user)
        if RequestAuthorUser.objects.filter(user=user, author=author).exists():
            request_form.delete()
            messages.success(request, 'You are unfollowed!!')  
            return redirect('books:author_detail', pk=pk, permanent=True)
        else:
            data = {
                'user': user.pk,
                'author': author.pk,
                'is_status': True
            }
            request_form = RequestAuthorUserForm(data=data)
            
            if request_form.is_valid():
                request_form.save()
                messages.success(request, "Follow request sent successfully!")
                return redirect('books:author_detail', pk=pk, permanent=True)
            else:
                messages.error(request, "Follow request sent unsuccessfully!")
                
          
        return render(request, 'books/author.html', {'author': author, 'request_form': request_form})
    
    def get(self, request, pk):
        author = Author.objects.get(pk=pk)
        user = self.request.user
        request_form = RequestAuthorUser.objects.filter(user=user, author=author).exists()
        author_book = BookAuthor.objects.filter(author=author.pk)
        return render(request, 'books/author.html', {'user': user,'author': author, 'request_form': request_form, 'author_book': author_book})
        

class AuthorUserChatView(LoginRequiredMixin, View):

    def post(self, request, pk, user_pk):
        author = Author.objects.get(pk=pk)
        user = self.request.user
        form = AuthorUserChatForm(data=request.POST)

        if form.is_valid():
            MessageToAuthor.objects.create(
                user=user,
                author=author,
                comment_user=form.cleaned_data['comment_user']
            )
            messages.success(request, 'Send message')
            return redirect('books:author_user_chat', pk=pk, user_pk=user.pk)
        else:
            messages.error(request, 'Unsend message')

        return render(request, 'books/author_user_chat.html', {'form': form})
    
    def get(self, request, pk, user_pk):
        author = Author.objects.get(pk=pk)
        user = CustomUser.objects.get(pk=user_pk)
        message = MessageToAuthor.objects.filter(author=author, user=user).order_by('-created_at')

        return render(request, 'books/author_user_chat.html', {'message': message, 'user': user, 'author': author})
    


class MessageToAuthorView(LoginRequiredMixin, View):

    def post(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        author = Author.objects.get(user=self.request.user)
        message_form = MessageToAuthorForm(data=request.POST)

        if message_form.is_valid():
            # message_form.save()
            MessageToAuthor.objects.create(
                user = user,
                author = author,
                comment_author = message_form.cleaned_data['comment_author'],
            )

            messages.success(request, 'Send message')
            return redirect('books:author_message', pk=pk, permanent=True)
        else:
            messages.error(request, 'Unsend message')

        return render(request, 'books/message_author.html', {'message_form': message_form})
    

    def get(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        author = Author.objects.get(user=self.request.user)
        message = MessageToAuthor.objects.filter(author=author, user=user).order_by('-created_at')

        return render(request, 'books/message_author.html', {'message': message})
        


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
            
        page_size = request.GET.get('page_size', 4)
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
    
    
class BookReviewEditView(LoginRequiredMixin, View):

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
    

class BookReviewConfirmDeleteView(LoginRequiredMixin, View):
    
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


class CreateBookView(UserPassesTestMixin, CreateView):
    form_class = BookForm
    queryset = Book.objects.all()
    success_url = reverse_lazy('lending_page')
    template_name = 'books/create_book.html'


class UpdateBookView(UserPassesTestMixin, UpdateView):
    form_class = BookForm
    queryset = Book.objects.all()
    template_name = 'books/edit_book.html'        

    def get_success_url(self):
        return reverse('books:detail', kwargs={'pk': self.object.pk})


class DeleteBookView(UserPassesTestMixin, DeleteView):
    queryset = Book.objects.all()
    template_name = 'books/delete_book.html'
    success_url = reverse_lazy('lending_page')


class CreateAuthorView(LoginRequiredMixin, View):
    
    def get(self, request):
        form = AuthorForm()
        return render(request, 'books/create_author.html', {'form': form})


    def post(self, request):
        form = AuthorForm(data=request.POST)
        if not Author.objects.filter(user=self.request.user).exists():
            if form.is_valid():
                Author.objects.create(
                    first_name = form.cleaned_data['first_name'],
                    last_name = form.cleaned_data['last_name'],
                    bio = form.cleaned_data['bio'],
                    user = self.request.user
                )

                return redirect(reverse('users:profile'))
        else:
            messages.success(request, 'Siz author lavozimidasiz')
        return render(request, 'books/create_author.html', {'form': form})

class UpdateAuthorView(LoginRequiredMixin, UpdateView):
    form_class = AuthorForm
    queryset = Author.objects.all()
    template_name = 'books/edit_author.html'

    def get_success_url(self):
        return reverse('books:author_detail', kwargs={'pk': self.object.pk})


class DeleteAuthorView(LoginRequiredMixin, DeleteView):
    queryset = Author.objects.all()
    template_name = 'books/delete_author.html'
    success_url = reverse_lazy('profile')

    

    
    
