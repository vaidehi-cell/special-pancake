from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("category_listing/<str:category>", views.category_listing, name="category_listing"),
    path("listing/<int:item_id>", views.listing, name="listing"),
    path("listing/<int:item_id>/add_comment", views.add_comment, name="add_comment"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_to_watchlist/<int:item_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:item_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("add_bid/<int:item_id>", views.add_bid, name="add_bid"),
    path("close_bid/<int:item_id>", views.close_bid, name="close_bid"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)