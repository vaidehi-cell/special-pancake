from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db.models import Max
from .models import User, Listing, Bid, Comment, Category

#form for new listing
class NewListingForm(forms.Form):
    item_name = forms.CharField(label="Item Name", widget=forms.TextInput())
    price = forms.IntegerField(label="Price")
    item_image = forms.ImageField(label="Image of the product")
    category_name = forms.CharField(label="Category")
    description = forms.CharField(label="Product Description", widget=forms.Textarea())
    
#Home page
def index(request):
    active_listings = Listing.objects.filter(is_closed=False)
    return render(request, "auctions/index.html", {
        "active_listings" : active_listings
    })

#to view closed listings
def closed_listings(request):
    closed_listings = Listing.objects.filter(is_closed=True)
    return render(request, "auctions/closed_listings.html", {
        "closed_listings" : closed_listings
    })

#to login
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

#to log out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

#to register new user
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
        except:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

#to view categories
def categories(request):
    all_categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "all_categories" : all_categories
    })
    
#to view category specific listings
def category_listing(request, category):
    cat = Category.objects.get(category_name=category)
    category_listings = Listing.objects.filter(category_name=cat)
    return render(request, "auctions/category_listing.html", {
        "category_listings": category_listings, "category" : category
    })
    
#to view a listing
def listing(request, item_id):
    if request.user.is_authenticated:
        is_in_watchlist = request.user.watchlists.filter(list_id=item_id).exists()  
        details = Listing.objects.get(list_id=item_id)
        comms = details.comments.all()
        return render(request, "auctions/active_listing.html", {
            "details" : details , "comms" : comms, "is_in_watchlist" : is_in_watchlist})
    else:
        try:
            details = Listing.objects.get(list_id=item_id)
            return render(request, "auctions/active_listing1.html", {
            "details" : details })
        except:
            return render(request, "auctions/error_page.html")

#to create a new listing
def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid():
            name_item = form.cleaned_data["item_name"]
            price_item = form.cleaned_data["price"]
            image_item = form.cleaned_data["item_image"]
            category_item = form.cleaned_data["category_name"]
            if(price_item > 0):
                try:
                    category_item = Category.objects.get(category_name=category_item)
                except:
                    category_item = Category(category_name=category_item)
                    category_item.save()
                description_item = form.cleaned_data["description"]
                new_listing = Listing(item=name_item, price=price_item, lister=request.user,item_image=image_item, category_name=category_item, description=description_item)
            try:
                assert new_listing.price > 0
                new_listing.save()
                active_listings = Listing.objects.filter(is_closed=False)
                return render(request, "auctions/index.html", {
                    "active_listings" : active_listings })
            except:
                return render(request, "auctions/error_page.html")
        else:
            return render(request, "auctions/create_listing.html", {
                "form" : NewListingForm()
        })
    else:
        return render(request, "auctions/create_listing.html", {
            "form" : NewListingForm()
        })

#to add a comment to a listing
def add_comment(request, item_id):
    listing = Listing.objects.get(list_id=item_id)
    if request.method == "POST":
        comment_data = request.POST.get("comment_data")
        new_comment = Comment.objects.create(comment_content=comment_data, commentor=request.user)
        new_comment.save()
        listing.comments.add(new_comment)
        is_in_watchlist = request.user.watchlists.filter(list_id=item_id).exists()    
        return render(request, "auctions/active_listing.html", {
            "details" : listing, "comms" : listing.comments.all(), "is_in_watchlist" : is_in_watchlist
        })
    else:
        return render(request, "auctions/active_listing.html", {
           "details" : listing, "comms" : listing.comments.all()
        })

#to view watchlist items        
def watchlist(request):
    watchlist = request.user.watchlists.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist" : watchlist
    })

#to add an item to watchlist   
def add_to_watchlist(request, item_id):
    listing = Listing.objects.get(list_id=item_id)
    listing.watchers.add(request.user)
    is_in_watchlist = True
    return render(request, "auctions/active_listing.html", {
           "details" : listing, "comms" : listing.comments.all(), "is_in_watchlist" : is_in_watchlist
        })   

#to remove an item from watchlist   
def remove_from_watchlist(request, item_id):
    listing = Listing.objects.get(list_id=item_id)
    listing.watchers.remove(request.user)
    watchlist = request.user.watchlists.all()
    return render(request, "auctions/watchlist.html", {
           "watchlist" : watchlist
        }) 

#to add a bid on listing    
def add_bid(request, item_id):
    listing = Listing.objects.get(list_id=item_id)
    if request.method == "POST":
        value = int(request.POST.get("bid_value"))
        all_bids = listing.bids.all()
        if all_bids:
            check = all_bids.aggregate(Max('bid_value'))["bid_value__max"] < value and listing.price <= value
        else:
            check = listing.price <= value
        if(all_bids is None or check):
            new_bid = Bid.objects.create(bid_value=value, bidder=request.user)
            new_bid.save()
            listing.bids.add(new_bid)
            is_in_watchlist = request.user.watchlists.filter(list_id=item_id).exists()    
            return render(request, "auctions/active_listing.html", {
                "details" : listing, "comms" : listing.comments.all(), "is_in_watchlist" : is_in_watchlist })
        else:
            is_in_watchlist = request.user.watchlists.filter(list_id=item_id).exists()
            return render(request, "auctions/active_listing.html", {
                "details" : listing, "comms" : listing.comments.all(), "is_in_watchlist" : is_in_watchlist, "message": "Invalid bid value"
            })
    else:
        return render(request, "auctions/active_listing.html", {
           "details" : listing, "comms" : listing.comments.all()
        })

#to close a listing
def close_bid(request, item_id):
    listing = Listing.objects.get(list_id = item_id)
    listing.is_closed = True
    all_bids = listing.bids.all()
    max_bid = all_bids.aggregate(Max('bid_value'))["bid_value__max"]
    max_bid = all_bids.get(bid_value=max_bid)
    winner = max_bid.bidder
    listing.winner = winner
    listing.save()
    is_in_watchlist = request.user.watchlists.filter(list_id=item_id).exists()    
    return render(request, "auctions/active_listing.html", {
        "details" : listing, "comms" : listing.comments.all(), "is_in_watchlist" : is_in_watchlist })