from django.urls import path, include

from . import views

from django.contrib import admin

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("make_listing", views.make_listing, name="make_listing"),
    path("listing/<str:listing_title>/", views.listing, name='listing'),
    path("listing/category/<str:category>/", views.filter_category, name="filter_category"),
    path("add_watchlist/<str:listing_title>/", views.add_watchlist, name="add_watchlist"),
    path('remove_watchlist/<str:listing_title>/', views.remove_watchlist, name='remove_watchlist'),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("listing/<str:listing_title>/add_comment/", views.add_comment, name="add_comment"),
    path("listing/<str:listing_title>/add_bid/", views.add_bid, name="add_bid"),
    path("listing/close_auction/<str:listing_title>", views.close_auction, name="close_auction")
]