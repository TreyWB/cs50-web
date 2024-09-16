from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("edit_listing/<int:listing_id>", views.edit_listing, name="edit_listing"),
    path("watchlist_added", views.watchlist_added, name="watchlist_added"),
    path("watchlist_removed", views.watchlist_removed, name="watchlist_removed"),
    path("new_bid", views.new_bid, name="new_bid"),
    path("close_listing", views.close_listing, name="close_listing"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    # TODO add path to show all user listings
    # TODO add path to see your watchlist
]
