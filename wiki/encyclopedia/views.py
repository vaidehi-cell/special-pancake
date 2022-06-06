#Imports
from turtle import textinput
from django.http import HttpResponse
from . import util
from django import forms
from django.shortcuts import render
import os, random, markdown

#Forms
class newPageForm(forms.Form):
    title = forms.CharField(label = "Title", widget = forms.TextInput(attrs={'placeholder': 'Single Word'}))
    description = forms.CharField(label = "Description", widget = forms.Textarea(attrs={'placeholder':'Data of entry in Markdown'}))

class deletePageForm(forms.Form):
    title = forms.CharField(label = "Title")

class editPageForm(forms.Form):
    info = forms.CharField(label = "Info", widget=forms.Textarea())

#Views

#To get all wiki entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
#To render a particular entry
def entry(request, page):
    text = util.get_entry(page)
    if text is None:
        return render(request, "encyclopedia/errorPage.html", {"message" : "No such entry exists!"})
    return render(request, "encyclopedia/getPage.html", {
        "page": text,
        "page_title": page})
   
#To render newPage page and create a new page 
def newPage(request):
    if request.method == "POST":
        form = newPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            details = form.cleaned_data["description"]
            if(util.get_entry(title) is None):
                util.save_entry(title, details)
            else:
                return render(request, "encyclopedia/errorPage.html", {
                    "message": "A page with same title already exists!"
                })
        else:
            return render(request, "encyclopedia/newPage.html", {
                "form": form })
    return render(request, "encyclopedia/newPage.html", {
        "form": newPageForm()} )
    
#To render a random wiki entry
def randomPage(request):
    randomfile = random.choice(os.listdir("entries/"))
    text = util.get_entry(randomfile[:-3])
    return render(request, "encyclopedia/getPage.html", {
        "page": text,
        "page_title": randomfile[:-3]})

#To render deletePage page and delete a wiki entry 
def deletePage(request):
    if request.method == "POST":
        form = deletePageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            title = "C:/Users/vaide/wiki/entries/" + title + ".md"
            try:
                os.remove(title)
                return render(request, "encyclopedia/errorPage.html", {
                "message": "Page deleted successfully!" })
            except:
                return render(request, "encyclopedia/errorPage.html", {
                "message": "No such page exists!" })
        else:
            return render(request, "encyclopedia/deletePage.html", {
                "form": form })
    return render(request, "encyclopedia/deletePage.html", {
        "form": deletePageForm()} )
  
#To search a wiki entry  
def searchPage(request):
    if request.method == "POST":
        title = request.POST.get("q")
        entries = [entry.lower() for entry in util.list_entries()]
        if title.lower() in entries:
            return entry(request, title)
        else:
            text = util.list_entries()
            if title == "":
                return index(request)
            matches = [entry for entry in text if title.lower() in entry.lower()]
            if(matches == []):
                return render(request, "encyclopedia/errorPage.html", {
                          "message": "No matching entry!"})
            return render(request, "encyclopedia/searchPage.html", {
                          "pages": matches})
    else:
        return render(request, "encyclopedia/index.html")


def editPage(request, page_title):
    
    pageData = util.get_entry(page_title)
    initial_dict = { 'info' : pageData }
    
    if request.method == "GET":
        
        if pageData is None:
            return render(request, "encyclopedia/errorPage.html", { "message" : "No such page exists!"})
        return render(request, "encyclopedia/editPage.html", {"form" : editPageForm(initial= initial_dict), "page_title" : page_title})
    
    elif request.method == "POST":
        form = editPageForm(request.POST)
        
        if form.is_valid():
            newData = form.cleaned_data["info"]
            util.save_entry(page_title, newData)
            return entry(request, page_title)
        else:
            return render(request, "encyclopedia/errorPage.html", {
                "message" : "Form not valid, please try again!" })
    