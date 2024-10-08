from django.db import models
from django.db.models import Max
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

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

    photo_url = models.URLField(null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Listing"
        verbose_name_plural = "Listings"

    def get_current_bid(self):
        highest_bid = Bids.objects.filter(listing=self).aggregate(Max('bid'))['bid__max']
        return highest_bid if highest_bid is not None else self.initial_bid

    def bid_count(self):
        return Bids.objects.filter(listing=self).count()

    def watchlist_count(self):
        return Watchlist.objects.filter(listing=self).count()


class Bids(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.PROTECT)
    bid = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Bid"
        verbose_name_plural = "Bids"


class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)

    def is_listing_watched(self):
        if Watchlist.objects.filter(listing_id=Listings.id, user_id=User.id).values('id'):
            return True
        else:
            return False


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    posted_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def comment_count(self):
        return Comments.objects.filter(listing=self).count()


class Winners(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    winning_bid = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Winner"
        verbose_name_plural = "Winners"