# Generated by Django 5.2 on 2025-04-13 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('institution_type', models.CharField(choices=[('school', 'School'), ('coaching', 'Coaching'), ('college', 'College')], max_length=20)),
                ('address', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('website', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
