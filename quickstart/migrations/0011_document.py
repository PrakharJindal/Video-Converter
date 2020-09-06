# Generated by Django 3.1 on 2020-09-04 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0010_list_vid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
