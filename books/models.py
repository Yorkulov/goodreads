from django.db import models
from users.models import CustomUser
from django.utils import timezone

from django.core.validators import MaxValueValidator, MinValueValidator


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    isbn = models.CharField(max_length=17)
    default_picture = models.ImageField(default='default_book.png')

    def __str__(self):
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class BookAuthor(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author_id.first_name} by {self.book_id.title}"


class BookReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    stars_given = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.first_name or self.user.username} by {self.book.title} ::: {self.stars_given} starts"



    
