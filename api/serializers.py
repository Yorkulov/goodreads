from rest_framework import serializers

from books.models import Book, BookReview
from users.models import CustomUser


# class BookSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=250)
#     description = serializers.CharField()
#     isbn = serializers.CharField(max_length=14)


# class UserSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=125)
#     first_name = serializers.CharField(max_length=150)
#     last_name = serializers.CharField(max_length=150)
#     email = serializers.CharField(max_length=125)


# class BookReviewSerializer(serializers.Serializer):
#     stars_given = serializers.IntegerField(min_value=1, max_value=5)
#     comment = serializers.CharField()
#     book_id = BookSerializer()
#     user_id = UserSerializer()


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['pk', 'title', 'description', 'isbn']


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['pk', 'username', 'first_name', 'last_name', 'email']


class BookReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BookReview
        fields = ('pk', 'stars_given', 'comment', 'user', 'book', 'book_id',  'user_id')


        