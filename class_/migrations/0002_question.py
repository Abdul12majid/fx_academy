# Generated by Django 4.2.2 on 2023-09-19 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class_', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(blank=True, max_length=50)),
                ('date_asked', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]