from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    def __str__(self):
        return f"{self.id}: {self.first_name} {self.last_name}"

class Category(models.Model):
    category_name = models.CharField(max_length=64, primary_key=True)    

    def __str__(self):
        return f"{self.category_name}"

class Bid(models.Model):
    bidId = models.AutoField(primary_key=True, auto_created=True)
    bid_value = models.IntegerField()
    bidder = models.ForeignKey(User, related_name="bids", on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f" Rs.{self.bid_value}: {self.bidder.username}"
    
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True, auto_created=True)
    comment_content = models.CharField(max_length=200)
    commentor = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.commentor.username} : {self.comment_content}"
    
class Listing(models.Model):
    list_id = models.IntegerField(primary_key=True, auto_created=True)
    item = models.CharField(max_length=64)
    price = models.IntegerField()
    lister = models.ForeignKey(User, related_name="listings", on_delete=models.CASCADE)
    item_image = models.ImageField(upload_to='images', null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(Comment)
    bids = models.ManyToManyField(Bid)
    category_name = models.ForeignKey(Category, related_name="listings", null=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=200,null=True)
    watchers = models.ManyToManyField(User, related_name="watchlists")
    is_closed = models.BooleanField(default=False)
    winner = models.ForeignKey(User, related_name="purchases", null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.list_id} {self.item}: Rs. {self.price}"
    
    def get_comments(self):
        return self.comments.all()