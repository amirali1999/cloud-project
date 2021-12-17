# Generated by Django 3.2.9 on 2021-12-05 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rank', models.IntegerField()),
                ('Name', models.CharField(max_length=255)),
                ('Platform', models.CharField(max_length=255)),
                ('Year', models.IntegerField()),
                ('Genre', models.CharField(max_length=255)),
                ('Publisher', models.CharField(max_length=255)),
                ('NA_Sales', models.DecimalField(decimal_places=2, max_digits=4)),
                ('EU_Sales', models.DecimalField(decimal_places=2, max_digits=4)),
                ('JP_Sales', models.DecimalField(decimal_places=2, max_digits=4)),
                ('Other_sales', models.DecimalField(decimal_places=2, max_digits=4)),
                ('Global_sales', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
    ]
