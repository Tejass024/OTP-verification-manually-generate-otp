# Generated by Django 4.1.4 on 2022-12-09 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_phoneotp'),
    ]

    operations = [
        migrations.AddField(
            model_name='phoneotp',
            name='validated',
            field=models.BooleanField(default=False, help_text='if it is true, that means user have validate otp correctly in second API'),
        ),
    ]