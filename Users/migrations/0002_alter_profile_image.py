# Generated by Django 5.1.3 on 2024-12-07 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(
                default="showa_default_pic.jpg", upload_to="profile_pics"
            ),
        ),
    ]
