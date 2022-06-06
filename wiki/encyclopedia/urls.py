from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.newPage, name="newPage"),
    path("deletepage", views.deletePage, name="deletePage"),
    path("randompage", views.randomPage, name="randomPage"),
    path("searchPage", views.searchPage, name="searchPage"),
    path("editPage/<str:page_title>", views.editPage, name="editPage"),
    path("wiki/<str:page>", views.entry, name="entry")
]
