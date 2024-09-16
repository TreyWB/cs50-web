from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Max

from .forms import CreateListingForm, BidForm
from .models import User, Listings, Watchlist, Bids, Winners


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "GET" and request.user.is_authenticated:
        form = CreateListingForm()
        return render(request, "auctions/create_listing.html", {
            "form": form
        })
    elif request.method == "POST" and request.user.is_authenticated:
        form = CreateListingForm(request.POST, request.FILES, user_id=request.user.id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index")) # TODO: redirect to the new listing
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form
            })
    else:
        return render(request, "auctions/error.html", {
            "message": "You must be logged in to create a listing."
        })


def listing(request, listing_id):
    listing = get_object_or_404(Listings, id=listing_id)
    form = BidForm(listing_id=listing_id)

    if request.user.is_authenticated:
        is_watched = Watchlist.objects.filter(listing_id=listing.id, user_id=request.user.id).exists()
    else:
        is_watched = False  # If the user is not authenticated, default to False

    winner = Winners.objects.filter(listing=listing).first()

    # Render the template with the context
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": form,
        "is_watched": is_watched,
        "winner": winner
    })


def watchlist_added(request):
    if not request.user.is_authenticated or request.method != "POST":
        return render(request, "auctions/error.html", {
            "message": "You must be logged in to add listings to your watchlist."
        })

    listing_id = request.POST.get("listing_id")
    user_id = request.user.id

    if not listing_id or not user_id:
        return render(request, "auctions/error.html", {
            "message": "Invalid request: listing_id or user_id is missing."
        })

    Watchlist.objects.create(listing_id=listing_id, user_id=user_id)
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


def watchlist_removed(request):
    if not request.user.is_authenticated or request.method != "POST":
        return render(request, "auctions/error.html", {
            "message": "You must be logged in to remove listings from your watchlist."
        })

    listing_id = request.POST.get("listing_id")
    user_id = request.user.id

    if not listing_id or not user_id:
        return render(request, "auctions/error.html", {
            "message": "Invalid request: listing_id or user_id is missing."
        })

    Watchlist.objects.filter(listing_id=listing_id, user_id=user_id).delete()
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

def new_bid(request):
    # Ensure listing_id is obtained correctly
    listing_id = request.POST.get("listing_id")
    # Ensure user_id is from the logged-in user
    user_id = request.user.id

    # Debugging: Print to ensure correct values
    print(f"Received listing_id: {listing_id}, user_id: {user_id}")

    # Ensure listing_id is a valid number
    if not listing_id or not listing_id.isdigit():
        return render(request, "auctions/error.html", {
            "message": "Invalid listing ID."
        })

    # Check if the request method is POST and the user is authenticated
    if request.method == "POST" and request.user.is_authenticated:
        # Initialize the BidForm with POST data and pass listing_id and user_id
        form = BidForm(request.POST, listing_id=int(listing_id), user_id=int(user_id))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))
        else:
            # If the form is not valid, show an error message
            return render(request, "auctions/error.html", {
                "message": "Invalid bid. Please try again."
            })
    else:
        # If the user is not authenticated or the method is not POST, show an error message
        return render(request, "auctions/error.html", {
            "message": "You must be logged in to place a bid."
        })

def close_listing(request):
    if request.method == "POST" and request.user.is_authenticated:
        listing_id = request.POST.get("listing_id")
        user_id = request.user.id

        if not listing_id or not user_id:
            return render(request, "auctions/error.html", {
                "message": "Invalid request: listing_id or user_id is missing."
            })

        # Fetch the listing object from the database
        listing = get_object_or_404(Listings, id=listing_id)

        # Check if the user is the owner of the listing
        if listing.user_id != user_id:
            return render(request, "auctions/error.html", {
                "message": "You are not the owner of this listing."
            })

        # Check if the listing is still open
        if not listing.is_active:  # Assuming `is_active` is a field in Listings model
            return render(request, "auctions/error.html", {
                "message": "Listing is already closed."
            })

        # Close the listing
        listing.is_active = False
        listing.save()

        winning_bid = Bids.objects.filter(listing=listing).aggregate(Max('bid'))['bid__max']
        winner = Bids.objects.filter(listing=listing).aggregate(Max('user_id'))['user_id__max']

        Winners.objects.create(listing=listing, winning_bid=winning_bid, user_id=winner)

        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    else:
        return render(request, "auctions/error.html", {
            "message": "You must be logged in to close a listing."
        })

def edit_listing(request):
    pass