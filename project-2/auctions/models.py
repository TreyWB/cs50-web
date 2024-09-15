from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.name

class Listings(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    initial_bid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    photo = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, null=True)
    watchlist_count = models.IntegerField(default=0)

    def get_current_bid(self):
        highest_bid = Bids.objects.filter(listing=self).aggregate(Max('bid'))['bid__max']
        return highest_bid if highest_bid is not None else self.initial_bid

    def bid_count(self):
        return Bids.objects.filter(listing=self).count()

class Bids(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.PROTECT)
    bid = models.DecimalField(max_digits=10, decimal_places=2)

class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)