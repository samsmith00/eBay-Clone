from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages


from .models import User, Category, Auction_Listing, Comments, Bids

 
def index(request):
    return render(request, "auctions/index.html", {
        "active_listings": Auction_Listing.objects.filter(isActive=True),
        "categories": Category.objects.all()
    })

def listing(request, listing_title):
    listing = Auction_Listing.objects.get(title=listing_title)
    in_watchlist = request.user in listing.watchlist.all()
    comments = Comments.objects.filter(listing=listing)
    highest_bid = Bids.objects.filter(listing=listing).order_by('-bid').first()
    owner = request.user.username == listing.owner.username
    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "in_watchlist": in_watchlist,
        "comments": comments,
        "highest_bid": highest_bid.bid if highest_bid else listing.price,
        "owner": owner
    })

def add_watchlist(request, listing_title):
    listing = Auction_Listing.objects.get(title=listing_title)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(listing_title,)))

def remove_watchlist(request, listing_title):
    listing = Auction_Listing.objects.get(title=listing_title)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=[listing_title]))

def watchlist(request):
    owner = request.user.username == listing.owner.username
    user = request.user
    listings = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "owner": owner
    })

def add_comment(request, listing_title):
    user = request.user
    listing = Auction_Listing.objects.get(title=listing_title)
    message = request.POST['new_comment']
    comment = Comments(
        owner=user,
        message=message,
        listing=listing
    )
    comment.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_title,)))

def add_bid(request, listing_title):
    user = request.user
    listing = Auction_Listing.objects.get(title=listing_title)
    bid_amount = float(request.POST['bid_value'])
    existing_bids = Bids.objects.filter(listing=listing)

    if existing_bids.exists():
        highest_bid = existing_bids.order_by('-bid').first().bid
    else: 
        highest_bid = listing.price
    
    if bid_amount > highest_bid:
        new_bid = Bids(
            listing=listing,
            owner=user,
            bid = bid_amount,
        )
        new_bid.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_title,)))

def close_auction(request, listing_title):
    listing = Auction_Listing.objects.get(title=listing_title)
    in_watchlist = request.user in listing.watchlist.all()
    comments = Comments.objects.filter(listing=listing)
    highest_bid = Bids.objects.filter(listing=listing).order_by('-bid').first()
    owner = request.user.username == listing.owner.username
    
    if request.method == 'POST':
       
        listing.isActive = False
        listing.save()

        winner = highest_bid.owner if highest_bid else None
        if winner:
            message = f"Congratulations! {winner.username} won the auction with a bid of {highest_bid.bid}"
        else:
            message = "No bids were placed on this listing."
        
        highest_bid = 0.0

        messages.success(request, message)
        
        return render(request, "auctions/listing_page.html", {
            "listing": listing,
            "in_watchlist": in_watchlist,
            "comments": comments,
            "highest_bid": highest_bid.bid if highest_bid else listing.price,
            "owner": owner,
            "message": message  
        })

    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "in_watchlist": in_watchlist,
        "comments": comments,
        "highest_bid": highest_bid.bid if highest_bid else listing.price,
        "owner": owner,
    })
     


def filter_category(request, category):
    if request.method == "POST":
        category_used = request.POST['category']
        category = Category.objects.get(category_name=category_used)
        return render(request, "auctions/index.html", {
            "active_listings": Auction_Listing.objects.filter(isActive=True, category=category),
            "categories": Category.objects.all()
        })

def make_listing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        allUsers = User.objects.all()
        return render(request, "auctions/make_listing.html", {
            "categories": allCategories,
            "users": allUsers
        })
    else:
        title = request.POST['listing_title']
        image = request.POST['image_url']
        price = request.POST['price']
        description = request.POST['description']
        category = request.POST['category']

        current_user = request.user
        category_data = Category.objects.get(category_name=category)

        new_listing = Auction_Listing(title=title, 
                                      image=image, 
                                      price=price,
                                      description=description,
                                      category=category_data,
                                      owner=current_user
                                      )
        new_listing.save()
        return HttpResponseRedirect(reverse('index'))

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
    


