from django.contrib import admin

from books.models import Book, Author, BookAuthor, BookReview

class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn')  # admin qismida search fieldini qo'shish
    list_display = ('pk', 'title', 'isbn')  # admin qismi jadvalida ko'rinadigan atributlar
    #list_filter = ('isbn')  # admin panelga filter xossasini qo'shish


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'username', 'email')
    list_display = ('first_name', 'last_name', 'email')


class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ('author_id', 'book_id')


class BookReviewAdmin(admin.ModelAdmin):
    search_fields = ('comment', 'stars_given')
    list_filter = ('stars_given', )  # starts bo'yicha filter qo'shish
    list_display = ('pk', 'comment', 'stars_given')


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)
