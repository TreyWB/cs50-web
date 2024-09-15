from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max


class User(AbstractUser):
    pass

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    initial_bid = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to="auctions/photos", null=True)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, null=True)
    watchlist_count = models.IntegerField(default=0)

    def get_current_bid(self):
        highest_bid = Bids.objects.filter(listing=self).aggregate(Max('bid'))['bid__max']
        return highest_bid if highest_bid is not None else self.initial_bid

class Bids(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT)
    bid = models.DecimalField(max_digits=10, decimal_places=2)

class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)