# Generated by Django 3.1.6 on 2024-02-11 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateur', '0006_panier_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offres',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='panier',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
