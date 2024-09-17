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
    path("my_watchlist", views.my_watchlist, name="my_watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category_name>", views.category_details, name="category_details"),
    path("listings/<int:user_id>", views.user_listings, name="user_listings"),
]
