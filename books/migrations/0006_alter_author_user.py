# Generated by Django 4.0 on 2023-10-15 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('books', '0005_remove_author_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.customuser'),
        ),
    ]
