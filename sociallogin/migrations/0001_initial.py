# Generated by Django 2.2 on 2019-12-10 12:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateSocial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.CharField(max_length=200)),
                ('filename', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SocialLogin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(max_length=500, verbose_name='Use Id')),
                ('provider', models.CharField(max_length=500, verbose_name='Service Provider')),
                ('username', models.CharField(max_length=500, verbose_name='Username')),
                ('full_name', models.CharField(max_length=500, verbose_name='Completename ')),
                ('EXTRA_PARAMS', models.TextField(max_length=1000, verbose_name='Text Field')),
            ],
            options={
                'verbose_name': 'Social Login',
                'verbose_name_plural': 'Social Login',
            },
        ),
        migrations.CreateModel(
            name='LoggedInUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='logged_in_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
