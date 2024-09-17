from django.contrib import admin
from .models import User, Categories, Listings, Bids, Watchlist, Comments, Winners

# Register your models here.
admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Listings)
admin.site.register(Bids)
admin.site.register(Watchlist)
admin.site.register(Comments)
admin.site.register(Winners)