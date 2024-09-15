from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("edit_listing", views.edit_listing, name="edit_listing"),
    path("watchlist-added", views.add_to_watchlist, name="watchlist_added"),
    path("new_bid", views.new_bid, name="new_bid"),
    # TODO add path to show all user listings
    # TODO add path to see your watchlist
]
