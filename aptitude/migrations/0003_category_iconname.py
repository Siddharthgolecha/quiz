# Generated by Django 3.2 on 2021-06-24 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aptitude', '0002_comment_questionid'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='iconName',
            field=models.CharField(default='ti-bar-chart', max_length=50),
        ),
    ]
