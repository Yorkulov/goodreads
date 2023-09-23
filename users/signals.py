from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        # print(f"Welcome to goodreads clone!,Hi, {instance.username}, Welcome to goodreads clone. Enjoy the books and review")
        send_mail(
            "Welcome to goodreads clone!",
            f"Hi, {instance.username}, Welcome to goodreads clone. Enjoy the books and review",
            "settesla19@gmail.com",
            [instance.email]
        )