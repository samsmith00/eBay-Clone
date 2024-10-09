from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
   pass

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category_name}"

class Auction_Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    price = models.FloatField()
    image = models.URLField(max_length=2000)
    isActive = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.title}"

class Bids(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='bidder')
    bid = models.FloatField(max_length=64, default=0.0)
    listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, blank=True, null=True, related_name='listing_bid')
    is_valid = models.BooleanField(default=True)
   
    def __str__(self):
        return f"{self.owner} \n Bid: {self.bid}"
    
class Comments(models.Model):
    message = models.CharField(max_length=500, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="author")
    listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, blank=True, null=True, related_name='listing')

    def __str__(self):
        return f"{self.owner} \n Comment: {self.message}"

''' 
    Lecture 4 video helpful times
        1:27:16
'''