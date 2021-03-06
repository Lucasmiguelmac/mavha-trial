# Generated by Django 3.1.1 on 2020-10-01 00:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=130)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
                ('description', models.TextField()),
                ('adults', models.IntegerField(default=1)),
                ('children', models.IntegerField(default=1)),
                ('pets_allowed', models.BooleanField(default=False)),
                ('base_price', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('cleaning_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('image_url', models.URLField(null=True)),
                ('weekly_discount', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('monthly_discount', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SpecialPrices',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.listing')),
            ],
        ),
    ]
