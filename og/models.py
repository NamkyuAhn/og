from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class ArtistEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    phone_number = models.CharField(max_length=13)
    birth_date = models.DateField(help_text="YYYY-MM-DD")
    gender = models.CharField(max_length=4)
    is_checked = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'artist_entries'

class Artist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    phone_number = models.CharField(max_length=13)
    birth_date = models.DateField(help_text="YYYY-MM-DD")
    gender = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'artists'

class Exhibition(models.Model):
    artist = models.ForeignKey('og.Artist', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    starting_date = models.DateField(help_text="YYYY-MM-DD")
    ending_date = models.DateField(help_text="YYYY-MM-DD")

    class Meta:
        db_table = 'exhibitions'

class Item(models.Model):
    artist = models.ForeignKey('og.Artist', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    size = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(500)])
    exhibition_item = models.ManyToManyField('og.Exhibition', through='og.ExhibitionItem', related_name='ex_item')
    class Meta:
        db_table = 'items'

class ExhibitionItem(models.Model):
    exhibition = models.ForeignKey('og.Exhibition', on_delete=models.CASCADE)
    item = models.ForeignKey('og.item', on_delete=models.CASCADE)
    class Meta:
        db_table = 'exhibition_items'