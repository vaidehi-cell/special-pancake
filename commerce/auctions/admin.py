from django.contrib import admin
from .models import Comment, Bid, Listing, Category, User
# Register your models here.
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(Category)