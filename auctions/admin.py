from django.contrib import admin

from .models import Auction_Listing, Category, User, Comments, Bids

# Register your models here.
admin.site.register(User)
admin.site.register(Auction_Listing)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(Bids)
