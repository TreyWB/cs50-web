from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CreateListingForm, BidForm
from .models import User, Listings


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
    listing = Listings.objects.get(id=listing_id)
    form = BidForm(listing_id=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": form
    })

def watchlist_added(request):
    pass


def edit_listing(request):
    pass


def new_bid(request):
    pass