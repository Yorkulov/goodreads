from django.urls import path

from books.views import BookDetailView, BookListView, BookReviewConfirmDeleteView, BookReviewDeleteView, BookReviewEditView, BookReviewView

app_name = 'books'

urlpatterns = [
    path('', BookListView.as_view(), name='list'),
    path('<int:pk>/', BookDetailView.as_view(), name='detail'),
    path('<int:pk>/review/', BookReviewView.as_view(), name='review'),
    path('<int:book_pk>/review/<int:review_pk>/edit/', BookReviewEditView.as_view(), name='review_edit'),
    path('<int:book_pk>/review/<int:review_pk>/confirmm-delete/', BookReviewConfirmDeleteView.as_view(), name='review_confirm_delete'),
    path('<int:book_pk>/review/<int:review_pk>/review/delete/', BookReviewDeleteView.as_view(), name='review_delete'),  
]
