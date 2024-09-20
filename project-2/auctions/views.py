from django.urls import reverse
from django.shortcuts import render
from django.db import IntegrityError
from django.db.models import Max, Count, ExpressionWrapper, Q, BooleanField
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout

from .forms import CreateListingForm, BidForm
from .models import User, Listings, Watchlist, Bids, Winners, Categories, Comments


def index(request):
    show_closed = request.GET.get("show_closed")

    if show_closed:
        listings = Listings.objects.all()
    else:
        listings = Listings.objects.filter(is_active=True)

    return render(request, "auctions/index.html", {
        'listings': listings
    })


def login_view(request):
    if request.method == "POST":
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
        categories = Categories.objects.all()

        return render(request, "auctions/create_listing.html", {
            "form": form,
            "categories": categories
        })
    elif request.method == "POST" and request.user.is_authenticated:
        form = CreateListingForm(request.POST, request.FILES, user_id=request.user.id)

        if form.is_valid():
            new_listing = form.save()
            listing_id = new_listing.id

            return HttpResponseRedirect(reverse("listing", args=[listing_id]))
        else:
            categories = Categories.objects.all()
            return render(request, "auctions/create_listing.html", {
                "form": form,
                "categories": categories
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
        is_watched = False

    winner = Winners.objects.filter(listing=listing).first()
    comments = Comments.objects.filter(listing=listing).all()
    comment_count = comments.count()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": form,
        "is_watched": is_watched,
        "winner": winner,
        "comments": comments,
        "comment_count": comment_count
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


def my_watchlist_removed(request):
    if not request.user.is_authenticated or request.method != "POST":
        return render(request, "auctions/error.html", {
            "message": "You must be logged in to remove a listing from your watchlist."
        })

    listing_id = request.POST.get("listing_id")
    user_id = request.user.id

    if not listing_id or not user_id:
        return render(request, "auctions/error.html", {
            "message": "Invalid request: listing_id or user_id is missing."
        })

    Watchlist.objects.filter(listing_id=listing_id, user_id=user_id).delete()
    return HttpResponseRedirect(reverse("my_watchlist"))


def new_bid(request):
    listing_id = request.POST.get("listing_id")
    user_id = request.user.id

    if not listing_id or not listing_id.isdigit():
        return render(request, "auctions/error.html", {
            "message": "Invalid listing ID."
        })

    if request.method == "POST" and request.user.is_authenticated:
        form = BidForm(request.POST, listing_id=int(listing_id), user_id=int(user_id))

        try:
            if form.is_valid():
                form.save()
            else:
                return render(request, "auctions/error.html", {
                    "message": "Invalid bid. Please try again."
                })

            return HttpResponseRedirect(reverse("listing", args=[listing_id]))
        except TypeError:
            return render(request, "auctions/error.html", {
                "message": "Invalid bid. Please try again."
            })

    else:
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

        listing = get_object_or_404(Listings, id=listing_id)

        if listing.user_id != user_id:
            return render(request, "auctions/error.html", {
                "message": "You are not the owner of this listing."
            })

        if not listing.is_active:
            return render(request, "auctions/error.html", {
                "message": "This listing has already been closed."
            })

        listing.is_active = False
        listing.save()

        if listing.initial_bid != listing.get_current_bid():
            winning_bid = Bids.objects.filter(listing=listing).aggregate(Max('bid'))['bid__max']
            winner = Bids.objects.filter(listing=listing).aggregate(Max('user_id'))['user_id__max']

            Winners.objects.create(listing=listing, winning_bid=winning_bid, user_id=winner)

        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    else:
        return render(request, "auctions/error.html", {
            "message": "You must be logged in to close a listing."
        })


def reopen_listing(request):
    if request.method == "POST" and request.user.is_authenticated:
        listing_id = request.POST.get("listing_id")
        user_id = request.user.id

        if not listing_id or not user_id:
            return render(request, "auctions/error.html", {
                "message": "Invalid request: listing_id or user_id is missing."
            })

        listing = get_object_or_404(Listings, id=listing_id)

        if listing.user_id != user_id:
            return render(request, "auctions/error.html", {
                "message": "You are not the owner of this listing."
            })

        if listing.is_active:
            return render(request, "auctions/error.html", {
                "message": "This listing is already open."
            })

        listing.is_active = True
        listing.save()

        if Winners.objects.filter(listing=listing).exists():
            Winners.objects.filter(listing=listing).delete()

        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    else:
        return render(request, "auctions/error.html", {
            "message": "You must be logged in to reopen a listing."
        })


def edit_listing(request, listing_id):
    listing = get_object_or_404(Listings, id=listing_id)
    categories = Categories.objects.all()

    if request.method == "GET" and request.user.is_authenticated:
        return render(request, "auctions/edit_listing.html", {
            "listing": listing,
            "categories": categories,
        })

    if not request.user.is_authenticated:
        return render(request, "auctions/error.html", {
            "message": "You must be logged in to edit a listing."
        })

    if listing.user != request.user:
        return render(request, "auctions/error.html", {
            "message": "You are not the owner of this listing."
        })

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        initial_bid = request.POST.get("initial_bid")
        category_id = request.POST.get("category")
        photo_url = request.POST.get("photo_url")

        listing.title = title
        listing.description = description
        listing.initial_bid = initial_bid
        listing.category = Categories.objects.get(id=category_id) if category_id else None

        if photo_url:
            listing.photo_url = photo_url

        listing.save()

        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    else:
        categories = Categories.objects.all()

        return render(request, "auctions/edit_listing.html", {
            "listing": listing,
            "categories": categories,
        })


def add_comment(request, listing_id):
    if request.method == "POST" and request.user.is_authenticated:
        comment = request.POST.get("comment")
        user_id = request.user.id
        listing = get_object_or_404(Listings, id=listing_id)

        if not comment or not user_id:
            return render(request, "auctions/error.html", {
                "message": "Invalid request: comment or user_id is missing."
            })

        Comments.objects.create(listing=listing, comment=comment, user_id=user_id)

        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    else:
        return render(request, "auctions/error.html", {
            "message": "You must be logged in to add a comment."
        })


def my_watchlist(request):
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user_id=request.user.id)
        listings = Listings.objects.filter(id__in=watchlist.values_list('listing_id', flat=True))

        # Probably just remove this its dumb
        listings = listings.annotate(
            is_watched=ExpressionWrapper(
                Q(id__in=watchlist.values_list('listing_id', flat=True)),
                output_field=BooleanField()
            )
        )

        return render(request, "auctions/my_watchlist.html", {
            "watchlist": watchlist,
            "listings": listings
        })
    else:
        return render(request, "auctions/error.html", {
            "message": "You must be logged in to view your watchlist."
        })


def categories(request):
    categories = Categories.objects.annotate(number_of_listings=Count('listings'))

    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category_details(request, category_name):
    category = get_object_or_404(Categories, name=category_name)
    listings = Listings.objects.filter(category=category)

    return render(request, "auctions/category_details.html", {
        "category": category,
        "listings": listings
    })


def user_listings(request, user_id):
    listing_user = get_object_or_404(User, id=user_id)

    if request.user.is_authenticated and request.user.id == user_id:
        listings = Listings.objects.filter(user=listing_user)
    else:
        listings = Listings.objects.filter(user=listing_user).exclude(is_active=0)

    return render(request, "auctions/user_listings.html", {
        "listing_user": listing_user,
        "listings": listings,
    })