# Generated by Django 4.2.3 on 2023-07-24 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_app', '0007_alter_item_categories'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ModelForPivot',
        ),
    ]
