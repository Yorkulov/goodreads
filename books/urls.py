from django.urls import path
from django.views.generic import TemplateView

from books.views import AuthorUserChatView, AuthorView, BookDetailView, BookListView, BookReviewConfirmDeleteView, BookReviewDeleteView, BookReviewEditView, BookReviewView, CreateAuthorView, CreateBookView, DeleteAuthorView, DeleteBookView, MessageToAuthorView, UpdateAuthorView, UpdateBookView

app_name = 'books'

urlpatterns = [
    path('', BookListView.as_view(), name='list'),
    path('author/<int:pk>/', AuthorView.as_view(), name='author_detail'),
    path('author/<int:pk>/users/chats/', MessageToAuthorView.as_view(), name='author_message'),
    path('author/<int:pk>/profile/chats/<int:user_pk>/', AuthorUserChatView.as_view(), name="author_user_chat"),
    path('<int:pk>/', BookDetailView.as_view(), name='detail'),
    path('<int:pk>/review/', BookReviewView.as_view(), name='review'),
    path('<int:book_pk>/review/<int:review_pk>/edit/', BookReviewEditView.as_view(), name='review_edit'),
    path('<int:book_pk>/review/<int:review_pk>/confirmm-delete/', BookReviewConfirmDeleteView.as_view(), name='review_confirm_delete'),
    path('<int:book_pk>/review/<int:review_pk>/review/delete/', BookReviewDeleteView.as_view(), name='review_delete'),  
    path('create/', CreateBookView.as_view(), name='book_create'),
    path('<int:pk>/update/', UpdateBookView.as_view(), name='book_update'),
    path('<int:pk>/delete/', DeleteBookView.as_view(), name='book_delete'),
    path('author/create/', CreateAuthorView.as_view(), name='create_author'),
    path('author/<int:pk>/update/', UpdateAuthorView.as_view(), name='update_author'),
    path('author/<int:pk>/delete/', DeleteAuthorView.as_view(), name='delete_author'),
    
]
