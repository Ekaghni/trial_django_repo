# Generated by Django 4.1 on 2022-11-14 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TempVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='temp/Image/')),
            ],
            options={
                'db_table': 'Temporary Images',
            },
        ),
    ]