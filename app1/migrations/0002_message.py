# Generated by Django 3.1.6 on 2021-07-26 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(blank=True, max_length=40, null=True, verbose_name='Тема сообщения')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст сообщения')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Емейл')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='writer_mes', to=settings.AUTH_USER_MODEL, verbose_name='Автор сообщения')),
            ],
        ),
    ]
