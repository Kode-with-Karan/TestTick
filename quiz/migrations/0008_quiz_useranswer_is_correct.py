# Generated by Django 5.2 on 2025-04-20 11:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_rename_is_correct_quiz_useranswer_is_selected'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz_useranswer',
            name='is_correct',
            field=models.CharField(choices=[('options_A', 'Options A'), ('options_B', 'Options B'), ('options_C', 'Options C'), ('options_D', 'Options D')], default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
    ]
