# Generated by Django 4.0 on 2023-10-15 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_alter_reviewlikes_likers'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ReviewLikes',
        ),
    ]