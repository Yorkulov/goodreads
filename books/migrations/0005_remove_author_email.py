# Generated by Django 4.0 on 2023-10-15 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_isbn'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='email',
        ),
    ]
