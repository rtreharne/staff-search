# Generated by Django 3.2 on 2022-05-09 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0008_keyword_frequency'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('url', models.URLField(default='https://github.com/rtreharne/staff-search-static/blob/main/University%20of%20Liverpool%20campus%20010621%200040.JPG?raw=true')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]
