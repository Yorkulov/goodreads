# Generated by Django 4.0 on 2023-10-15 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('books', '0006_alter_author_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewLikes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likers', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.customuser')),
                ('review', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='books.bookreview')),
            ],
        ),
    ]
