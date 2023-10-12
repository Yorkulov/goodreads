from django import forms

from books.models import Author, BookReview, MessageToAuthor, RequestAuthorUser


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ('first_name', 'last_name')


class BookReviewForm(forms.ModelForm):
    stars_given = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = BookReview
        fields = ('stars_given', 'comment')

class RequestAuthorUserForm(forms.ModelForm):
    
    class Meta:
        model = RequestAuthorUser
        fields = ('author', 'user', 'is_status')
    

class MessageToAuthorForm(forms.ModelForm):

    class Meta:
        model = MessageToAuthor
        fields = ('comment_user', )


class AuthorUserChatForm(forms.ModelForm):

    class Meta:
        model = MessageToAuthor
        fields = ('comment_author', )
