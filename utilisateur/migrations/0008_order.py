# Generated by Django 3.1.6 on 2024-02-12 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateur', '0007_auto_20240211_2202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=100)),
                ('libelle', models.CharField(max_length=1000)),
                ('item', models.IntegerField()),
                ('prix', models.FloatField()),
                ('slug', models.SlugField(blank=True)),
                ('PUBKEY', models.CharField(blank=True, max_length=3000)),
            ],
        ),
    ]